import json
import boto3

comprehend = boto3.client('comprehend')

def lambda_handler(event, context):
    print("Received event:", event)

    # Check if 'body' exists in the event (indicating it's from API Gateway)
    if 'body' in event:
        body = json.loads(event['body'])
        reviews = body.get('reviews', [])
    else:
        reviews = event.get('reviews', [])

    # Analyze sentiments for each review
    results = []
    for review in reviews:
        sentiment_response = comprehend.detect_sentiment(Text=review, LanguageCode='en')
        sentiment = sentiment_response.get('Sentiment', 'UNKNOWN')
        results.append({
            'review': review,
            'sentiment': sentiment
        })

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        },
        'body': json.dumps({
            'results': results
        })
    }
