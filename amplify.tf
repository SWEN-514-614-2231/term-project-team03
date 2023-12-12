resource "aws_amplify_app" "uniview_app" {
  name = "uniview-app"

  oauth_token = var.github_oauth_token
  repository  = var.github_repo_url

  environment_variables = {
    "S3_BUCKET_RAW"        = aws_s3_bucket.uniview_fetchdata.bucket
    "S3_BUCKET_REVIEWS"    = aws_s3_bucket.uniview_preprocessing.bucket
    "S3_BUCKET_ANALYZED"   = aws_s3_bucket.uniview_analyzed.bucket
    "DYNAMODB_TABLE"       = aws_dynamodb_table.UniversityReviews.name
  }

  auto_branch_creation_config {
    #patterns = ["feature/*"]
    }
}
