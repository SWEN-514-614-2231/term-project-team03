resource "aws_s3_bucket" "uniview_fetchdata" {
  bucket = "uniview-fetchdata-swen614-team3"
  acl    = "private"
}

resource "aws_s3_bucket" "uniview_preprocessing" {
  bucket = "uniview-preprocessing-swen614-team3"
  acl    = "private"
}

resource "aws_s3_bucket" "uniview_analyzed" {
  bucket = "uniview-analyzed-swen614-team3"
  acl    = "private"
}

resource "aws_s3_bucket" "uniview_dynamodb" {
  bucket = "uniview-dynamodb-swen614-team3"
  acl    = "private"
}

resource "aws_s3_bucket" "uniview_synthetic" {
  bucket = "uniview-synthetic-swen614-team3"
  acl ="private"
}

resource "aws_s3_bucket_object" "synthetic_reviews" {
  bucket = aws_s3_bucket.uniview_synthetic.bucket
  key    = "synthetic_reviews.json"
  source = "synthetic_reviews.json"  
  acl ="private"
}

resource "aws_s3_bucket" "uniview_scripts" {
  bucket = "uniview-scripts-swen614-team3"
  acl    = "private"
}

resource "aws_s3_bucket_object" "analyzed_reviews" {
  bucket = aws_s3_bucket.uniview_analyzed.bucket
  key    = "analyzed-reviews.zip"
  source = "analyzed-reviews.zip"
  acl    = "private"
}
