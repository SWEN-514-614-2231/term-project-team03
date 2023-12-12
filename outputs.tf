output "s3_bucket_raw" {
  value = aws_s3_bucket.uniview_fetchdata.bucket
}

output "s3_bucket_reviews" {
  value = aws_s3_bucket.uniview_preprocessing.bucket
}

