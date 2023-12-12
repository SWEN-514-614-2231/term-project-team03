import json
import boto3
from sklearn.feature_extraction.text import TfidfVectorizer
# Initialize S3 and Comprehend clients
comprehend = boto3.client('comprehend', region_name='us-east-2')
s3_client = boto3.client('s3', region_name='us-east-2')
preprocessed_data_bucket = 'uniview-preprocessing-swen614-team3'
analyzed_data_bucket = 'uniview-analyzed-swen614-team3'
def get_file_from_s3(bucket_name, key):
    print(f"Fetching file from S3: {key}")
    object_content = s3_client.get_object(Bucket=bucket_name, Key=key)['Body'].read().decode('utf-8')
    return json.loads(object_content)
def save_to_s3(bucket_name, key, content):
    print(f"Saving file to S3: {key}")
    s3_client.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(content))
def analyze_sentiment(text):
    print("Analyzing sentiment...")
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return response['Sentiment'], response['SentimentScore']
def extract_keywords(texts, n=5):
    print("Extracting keywords...")
    vectorizer = TfidfVectorizer(max_df=1.0, stop_words='english', max_features=10000)
    tfidf = vectorizer.fit_transform(texts)
    feature_array = vectorizer.get_feature_names_out()
    keywords = []
    for text_vector in tfidf:
        tfidf_sorting = text_vector.tocoo().col
        top_keywords = [feature_array[i] for i in tfidf_sorting[:n]]
        keywords.append(top_keywords)
    return keywords
print("Fetching cleaned data from S3...")
cleaned_files = s3_client.list_objects_v2(Bucket=preprocessed_data_bucket, Prefix='cleaned_').get('Contents', [])
print(f"Found {len(cleaned_files)} files to process.")
for file in cleaned_files:
    data_key = file['Key']
    if "analyzed" in data_key:
        continue
    print(f"Processing file: {data_key}")
    reviews = get_file_from_s3(preprocessed_data_bucket, data_key)
    analyzed_reviews = []
    for review_text in reviews:
        if not review_text.strip():
            continue
        sentiment, sentiment_score = analyze_sentiment(review_text)
        keywords = extract_keywords([review_text])
        analyzed_review = {
            'text': review_text,
            'sentiment': sentiment,
            'sentiment_score': sentiment_score,
            'keywords': keywords,
            'positive_keywords': [] if sentiment != 'POSITIVE' else keywords,
            'negative_keywords': [] if sentiment != 'NEGATIVE' else keywords
        }
        analyzed_reviews.append(analyzed_review)
    output_key = 'analyzed_' + data_key.split('/')[-1]
    save_to_s3(analyzed_data_bucket, output_key, analyzed_reviews)
print("Finished processing all files.")
