resource "aws_dynamodb_table" "UniversityReviews" {
  name           = "UniversityReviews"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "university_name"
  range_key      = "review_timestamp"

  attribute {
    name = "university_name"
    type = "S"
  }

  attribute {
    name = "review_timestamp"
    type="N"
    }
}
