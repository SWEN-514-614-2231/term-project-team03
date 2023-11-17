import boto3
import json
import time

aws_region = 'us-east-2'

s3_client = boto3.client('s3', region_name=aws_region)
dynamodb = boto3.resource('dynamodb', region_name=aws_region)

bucket_name = 'uniview-analyzed-data'

table_name = 'UniversityReviews'

table = dynamodb.Table(table_name)

def get_file_from_s3(bucket_name, key):
    object_content = s3_client.get_object(Bucket=bucket_name, Key=key)['Body'].read().decode('utf-8')
    return json.loads(object_content)

def insert_into_dynamodb(data, university_name):
    for review in data:

        user_id = f"{university_name}_{int(time.time())}"

        item = {
            'university_name': university_name,  
            'userId': user_id,
            'itemId': university_name,
            'review_timestamp': review.get('review_timestamp', int(time.time())),  
            'eventValue': review['sentiment'], 
            'eventType': 'review', 
            'keywords': ",".join(review['keywords'][0]),  
            'text': review['text']
        }
        table.put_item(Item=item)

def process_files():
    files = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='analyzed_cleaned_')['Contents']
    
    for file in files:
        file_key = file['Key']

        university_name = file_key.replace('analyzed_cleaned_', '').replace('.json', '').replace('_', ' ')
        
        data = get_file_from_s3(bucket_name, file_key)
        insert_into_dynamodb(data, university_name)

process_files()
