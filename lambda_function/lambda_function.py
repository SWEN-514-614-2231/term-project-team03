import json
import requests
import boto3

# Initialize the Secrets Manager and S3 client
secrets_client = boto3.client('secretsmanager')
s3_client = boto3.client('s3')

universities = [
    "Massachusetts Institute of Technology (MIT)",
    "Stanford University",
    "Harvard University",
    "California Institute of Technology (Caltech)",
    "University of Oxford",
    "University of Cambridge",
    "ETH Zurich - Swiss Federal Institute of Technology",
    "University of Chicago",
    "Imperial College London",
    "University College London (UCL)",
    "National University of Singapore (NUS)",
    "Nanyang Technological University, Singapore (NTU)",
    "Tsinghua University",
    "Ecole Polytechnique Federale de Lausanne (EPFL)",
    "University of Pennsylvania",
    "Yale University",
    "Peking University",
    "Princeton University",
    "University of Edinburgh",
    "University of California, Berkeley (UCB)",
    "Columbia University",
    "University of California, Los Angeles (UCLA)",
    "University of Michigan-Ann Arbor",
    "University of Hong Kong (HKU)",
    "University of Toronto",
    "University of Tokyo",
    "Johns Hopkins University",
    "University of Manchester",
    "Northwestern University",
    "Fudan University",
    "University of California, San Diego (UCSD)",
    "University of Sydney",
    "University of Melbourne",
    "University of British Columbia",
    "Hong Kong University of Science and Technology (HKUST)",
    "Duke University",
    "University of New South Wales (UNSW Sydney)",
    "University of Queensland",
    "Korea Advanced Institute of Science and Technology (KAIST)",
    "London School of Economics and Political Science (LSE)",
    "Zhejiang University",
    "Shanghai Jiao Tong University",
    "McGill University",
    "Brown University",
    "University of Bristol",
    "University of Wisconsin-Madison",
    "University of Warwick",
    "University of Amsterdam",
    "University of Texas at Austin",
    "Carnegie Mellon University",
    "University of Washington",
    "University of Zurich",
    "University of Illinois Urbana-Champaign",
    "University of California, Santa Barbara (UCSB)",
    "Australian National University",
    "University of California, Davis (UCD)",
    "New York University (NYU)",
    "Seoul National University (SNU)",
    "University of North Carolina, Chapel Hill",
    "Delft University of Technology",
    "University of Southampton",
    "King's College London",
    "University of Copenhagen",
    "Georgia Institute of Technology",
    "University of Auckland",
    "Lomonosov Moscow State University",
    "University of Glasgow",
    "Kyoto University",
    "University of California, Irvine (UCI)",
    "University of Birmingham",
    "Osaka University",
    "University of Sheffield",
    "Ludwig-Maximilians-Universitat Munchen",
    "University of St Andrews",
    "University of Leeds",
    "National Taiwan University (NTU)",
    "Tohoku University",
    "University of Nottingham",
    "Lund University",
    "Technical University of Munich",
    "University of Oslo",
    "KU Leuven",
    "University of Helsinki",
    "Durham University",
    "University of Western Australia (UWA)",
    "University of Geneva",
    "Korea University",
    "University of Vienna",
    "Yonsei University",
    "University of Alberta",
    "University of Science and Technology of China",
    "University of Liverpool",
    "University of Groningen",
    "University of Basel"
]


def get_google_places_api_key():
    # Retrieve API key from Secrets Manager
    response = secrets_client.get_secret_value(SecretId='Places_API')
    api_key = json.loads(response['SecretString'])['GooglePlacesAPIKey']
    return api_key

def lambda_handler(event, context):
    # Get the API Key
    api_key = get_google_places_api_key()

    for university in universities:
        try:
            # Define the endpoint URL to search for the university and obtain its Place ID
            search_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={university.replace(' ', '%20')}&inputtype=textquery&fields=place_id&key={api_key}"
        
            response = requests.get(search_url)
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            data = response.json()

            # Assuming the first result is the most relevant
            if data['candidates']:
                place_id = data['candidates'][0]['place_id']
            else:
                print(f"No candidates found for {university}")
                continue  # Move to the next university if no Place ID found

            # Fetch detailed information using the Place ID
            details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
            details_response = requests.get(details_url)
            details_response.raise_for_status()
            details_data = details_response.json()

            # Store the data in the S3 bucket with a unique key based on the university name
            s3_key = f"{university.replace(' ', '-').lower()}.json"
            s3_client.put_object(Bucket='places-reviews-uniview', Key=s3_key, Body=json.dumps(details_data))
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {university}: {str(e)}")
            continue

    return {
        'statusCode': 200,
        'body': 'Data for all universities fetched and stored successfully!'
    }
