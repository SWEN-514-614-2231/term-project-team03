import boto3
import csv
from io import StringIO

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UniversityReviews')

def read_csv_from_s3(bucket, key):
    """Read CSV file from S3 bucket."""
    response = s3_client.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')
    return content

def process_csv_data(csv_data):
    """Process CSV data and write to DynamoDB."""
    rows = csv.DictReader(StringIO(csv_data), delimiter='\t')

    for row in rows:
        item = {
            'university_name': row['ITEM_ID'],
            'review_timestamp': int(row['TIMESTAMP']),
            'event_type': row['EVENT_TYPE'],
            'event_value': float(row['EVENT_VALUE']),
            'item_id_1': row['ITEM_ID_1'],
            'keywords': row['KEYWORDS'],
            'text': row['TEXT'],
            'user_id': row['USER_ID'],
            'positive_keywords': row['POSITIVE_KEYWORDS'],
            'negative_keywords': row['NEGATIVE_KEYWORDS'],
            'positive_score': float(row['POSITIVE_SCORE']),
            'negative_score': float(row['NEGATIVE_SCORE']),
            'neutral_score': float(row['NEUTRAL_SCORE'])
        }
        table.put_item(Item=item)

def process_csv_file(bucket, key):
    """Main processing function."""
    csv_data = read_csv_from_s3(bucket, key)
    process_csv_data(csv_data)

if __name__ == '__main__':
    process_csv_file('uniview_dynamodb', 'interactions.csv')
