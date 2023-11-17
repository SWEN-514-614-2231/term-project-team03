import json
import re
import boto3

s3_client = boto3.client('s3')
bucket_name = 'places-reviews-uniview'
bucket_name2 = 'places-reviews-uniview2'
def get_data_from_s3(key):
    response = s3_client.get_object(Bucket=bucket_name, Key=key)
    data = json.loads(response['Body'].read().decode('utf-8'))
    return data

def extract_reviews(data):
    reviews = data.get('result', {}).get('reviews', [])
    return [review.get('text', '') for review in reviews]

def clean_text(text):
    # Remove URLs, special characters, and numbers
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\@\w+|\#', '', text)
    text = re.sub('[^a-zA-Z\s]', '', text)
    
    # Convert to lowercase
    text = text.lower()
    
    return text

def lambda_handler(event, context):
    # Fetch the list of all keys (files) in the S3 bucket
    s3_keys = [item['Key'] for item in s3_client.list_objects(Bucket=bucket_name)['Contents']]
    
    all_cleaned_reviews = []
    
    for s3_key in s3_keys:
        raw_data = get_data_from_s3(s3_key)
        reviews = extract_reviews(raw_data)
        cleaned_reviews = [clean_text(review) for review in reviews]
        all_cleaned_reviews.extend(cleaned_reviews)
        
        # Optional: Store cleaned reviews back in S3 or any other destination
        s3_client.put_object(Bucket=bucket_name2, Key=f"cleaned_{s3_key}", Body=json.dumps(cleaned_reviews))
    
    return {
        'statusCode': 200,
        'body': f'Processed {len(all_cleaned_reviews)} reviews!'
    }
