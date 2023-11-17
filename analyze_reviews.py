import json
import boto3
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize S3 and Comprehend clients
comprehend = boto3.client('comprehend', region_name='us-east-2')
s3_client = boto3.client('s3', region_name='us-east-2')

preprocessed_data_bucket = 'uniview-preprocessed-data'
analyzed_data_bucket = 'uniview-analyzed-data'

def get_file_from_s3(bucket_name, key):
    object_content = s3_client.get_object(Bucket=bucket_name, Key=key)['Body'].read().decode('utf-8')
    return json.loads(object_content)

def save_to_s3(bucket_name, key, content):
    s3_client.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(content))

def analyze_sentiment(text):
    return comprehend.detect_sentiment(Text=text, LanguageCode='en')['Sentiment']

def extract_keywords(texts, n=5):
    vectorizer = TfidfVectorizer(max_df=1.0, stop_words='english', max_features=10000)
    tfidf = vectorizer.fit_transform(texts)
    feature_array = vectorizer.get_feature_names_out()
    keywords = []
    for text_vector in tfidf:
        tfidf_sorting = text_vector.tocoo().col
        top_keywords = [feature_array[i] for i in tfidf_sorting[:n]]
        keywords.append(top_keywords)
    return keywords

# Fetch cleaned data from the Preprocessed Data Bucket
cleaned_files = s3_client.list_objects_v2(Bucket=preprocessed_data_bucket, Prefix='cleaned_')['Contents']
for file in cleaned_files:
    data_key = file['Key']
    
    # Skip files that have already been analyzed
    if "analyzed" in data_key:
        continue
    
    reviews = get_file_from_s3(preprocessed_data_bucket, data_key)
    analyzed_reviews = []

    # Perform sentiment analysis and keyword extraction
    for review_text in reviews:
        if not review_text.strip():
            continue
        analyzed_review = {
            'text': review_text,
            'sentiment': analyze_sentiment(review_text),
            'keywords': extract_keywords([review_text])
        }
        analyzed_reviews.append(analyzed_review)

    # Save results back to the Analyzed Data Bucket
    output_key = 'analyzed_' + data_key.split('/')[-1]
    save_to_s3(analyzed_data_bucket, output_key, analyzed_reviews)
