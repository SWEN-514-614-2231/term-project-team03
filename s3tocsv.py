import json
import boto3
import csv
import time

# Initialize S3 client
s3_client = boto3.client('s3', region_name='us-east-2')

def get_file_from_s3(bucket_name, key):
    object_content = s3_client.get_object(Bucket=bucket_name, Key=key)['Body'].read().decode('utf-8')
    return json.loads(object_content)

def upload_file_to_s3(bucket_name, file_name, key):
    with open(file_name, 'rb') as file:
        s3_client.upload_fileobj(file, bucket_name, key)

def process_file(file_key, start_timestamp, start_user_id):
    json_data = get_file_from_s3('uniview-analyzed-data', file_key)
    reviews_data = []
    current_timestamp = start_timestamp
    current_user_id = start_user_id

    for review in json_data:
        event_value = {'POSITIVE': 1.0, 'NEGATIVE': 0.0, 'NEUTRAL': 0.5, 'MIXED': 0.5}.get(review['sentiment'], 0.5)
        positive_keywords = ', '.join([kw for sublist in review.get('positive_keywords', []) for kw in sublist])
        negative_keywords = ', '.join([kw for sublist in review.get('negative_keywords', []) for kw in sublist])

        reviews_data.append([
            file_key.replace('analyzed_cleaned_', '').replace('_details.json', '').replace('_', ' '),  # ITEM_ID
            current_timestamp,  # TIMESTAMP
            'review',  # EVENT_TYPE
            event_value,  # EVENT_VALUE
            f"{file_key.replace('analyzed_cleaned_', '').replace('_details.json', '').replace('_', ' ')}_{current_timestamp}",  # ITEM_ID_1
            ', '.join([kw for sublist in review.get('keywords', []) for kw in sublist]),  # KEYWORDS
            review['text'],  # TEXT
            f"User_{current_user_id}",  # USER_ID
            positive_keywords,  # POSITIVE_KEYWORDS
            negative_keywords,   # NEGATIVE_KEYWORDS
            review['sentiment_score'].get('Positive', 0.0),  # Positive Sentiment Score
            review['sentiment_score'].get('Negative', 0.0),  # Negative Sentiment Score
            review['sentiment_score'].get('Neutral', 0.0)   # Neutral Sentiment Score
        ])

        current_user_id += 1
        current_timestamp += 1
      
    return reviews_data, current_timestamp, current_user_id

def write_to_csv(filename, data, fields):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        writer.writerows(data)

def process_all_files():
    interactions = []
    start_timestamp = int(time.time())
    start_user_id = 0

    response = s3_client.list_objects_v2(Bucket='uniview-analyzed-data')
    for file in response.get('Contents', []):
        file_key = file['Key']
        if file_key.endswith('.json'):
            reviews_data, start_timestamp, start_user_id = process_file(file_key, start_timestamp, start_user_id)
            interactions.extend(reviews_data)

    # Write interactions to CSV file
    interactions_fields = ['ITEM_ID', 'TIMESTAMP', 'EVENT_TYPE', 'EVENT_VALUE', 'ITEM_ID_1', 'KEYWORDS', 'TEXT', 'USER_ID', 'POSITIVE_KEYWORDS', 'NEGATIVE_KEYWORDS', 'POSITIVE_SCORE', 'NEGATIVE_SCORE', 'NEUTRAL_SCORE']    interactions_csv = 'interactions.csv'
    write_to_csv(interactions_csv, interactions, interactions_fields)

    # Upload CSV file to S3
    upload_file_to_s3('uniview-dynamodb', interactions_csv, 'interactions.csv')

process_all_files()
