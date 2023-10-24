import json
import boto3
import random

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Log the received event for debugging purposes
    print("Received event:", event)

    # Fetch the data from the S3 bucket
    response = s3_client.get_object(Bucket='places-reviews-uniview', Key='data.json')
    file_content = response['Body'].read().decode('utf-8')
    data = json.loads(file_content)

    # Extract reviews
    reviews = [review['text'] for review in data.get('result', {}).get('reviews', [])]

    # Shuffle the reviews
    random.shuffle(reviews)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        },
        'body': json.dumps({
            'reviews': reviews
        })
    }
