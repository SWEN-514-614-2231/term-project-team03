import json
import re
import boto3

s3_client = boto3.client('s3')

# Update these bucket names according to your setup
fetch_data_bucket = 'uniview-raw-data'
preprocessed_data_bucket = 'uniview-preprocessed-data'

def get_data_from_s3(bucket, key):
    response = s3_client.get_object(Bucket=bucket, Key=key)
    data = json.loads(response['Body'].read().decode('utf-8'))
    return data

def extract_reviews(data):
    reviews = data.get('result', {}).get('reviews', [])
    return [review.get('text', '') for review in reviews]

def clean_text(text):
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\@\w+|\#', '', text)
    text = re.sub('[^a-zA-Z\s]', '', text)
    text = text.lower()
    return text

def lambda_handler(event, context):
    try:
        s3_objects = s3_client.list_objects_v2(Bucket=fetch_data_bucket)
        if 'Contents' in s3_objects:
            s3_keys = [item['Key'] for item in s3_objects['Contents']]
        else:
            return {'statusCode': 200, 'body': 'No files found in the fetch data bucket'}

        all_cleaned_reviews = []
        
        for s3_key in s3_keys:
            raw_data = get_data_from_s3(fetch_data_bucket, s3_key)
            reviews = extract_reviews(raw_data)
            cleaned_reviews = [clean_text(review) for review in reviews]
            all_cleaned_reviews.extend(cleaned_reviews)
            
            s3_client.put_object(Bucket=preprocessed_data_bucket, Key=f"cleaned_{s3_key}", Body=json.dumps(cleaned_reviews))
        
        return {
            'statusCode': 200,
            'body': f'Processed {len(all_cleaned_reviews)} reviews!'
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'An error occurred: {str(e)}'
        }
