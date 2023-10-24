import json
import requests
import boto3

# Initialize the Secrets Manager and S3 client
secrets_client = boto3.client('secretsmanager')
s3_client = boto3.client('s3')

def get_google_places_api_key():
    # Retrieve API key from Secrets Manager
    response = secrets_client.get_secret_value(SecretId='Places_API')
    api_key = json.loads(response['SecretString'])['GooglePlacesAPIKey']
    return api_key

def lambda_handler(event, context):
    # Get the API Key
    api_key = get_google_places_api_key()
    
    # Define the endpoint URL to search for "Harvard University" and obtain its Place ID
    search_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=Harvard%20University&inputtype=textquery&fields=place_id&key={api_key}"
    
    response = requests.get(search_url)
    data = response.json()

    # Assuming the first result is the most relevant
    if data['candidates']:
        place_id = data['candidates'][0]['place_id']
    else:
        return {
            'statusCode': 404,
            'body': 'Place ID not found'
        }

    # Fetch detailed information using the Place ID
    details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
    details_response = requests.get(details_url)
    details_data = details_response.json()

    # Store the data in the S3 bucket
    s3_client.put_object(Bucket='places-reviews-uniview', Key='data.json', Body=json.dumps(details_data))
    
    return {
        'statusCode': 200,
        'body': 'Data fetched and stored successfully!'
    }

