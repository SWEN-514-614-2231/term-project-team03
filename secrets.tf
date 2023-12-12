resource "aws_secretsmanager_secret" "google_api_key" {
  name = "GoogleAPIKey_v33"
}

resource "aws_secretsmanager_secret_version" "google_api_key_value" {
  secret_id     = aws_secretsmanager_secret.google_api_key.id
  secret_string = "{\"GooglePlacesAPIKey\":\"AIzaSyCRLFTtqkYmQf6rj21Xv95lHOBfnjxwBcY\"}"
}
