resource "aws_s3_bucket_acl" "places-reviews-uniview" {
  bucket = "places-reviews-uniview"  # Replace with a globally unique bucket name

  acl    = "private"  # Access control for the bucket (private, public-read, public-read-write, etc.)

  
}

resource "aws_iam_policy" "s3_bucket_policy"{
    name = "s3_bucket_policy_for_iam_user"

policy = <<EOF
{
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": "*",
          "Action": [
            "s3:GetObject",
            "s3:PutObject",
            "s3:DeleteObject",
            "s3:ListBucket"
          ],
          "Resource": [
            "arn:aws:s3:::${aws_s3_bucket_acl.places-reviews-uniview.bucket}",
            "arn:aws:s3:::${aws_s3_bucket_acl.places-reviews-uniview2.bucket}",
            "arn:aws:s3:::${aws_s3_bucket_acl.places-reviews-uniview3.bucket}"
          ]
        }
      ]
    }
  EOF                   
}



resource "aws_s3_bucket_acl" "places-reviews-uniview2" {
  bucket = "places-reviews-uniview2"  # Replace with a globally unique bucket name

  acl    = "private"  # Access control for the bucket (private, public-read, public-read-write, etc.)
}

resource "aws_s3_bucket_acl" "places-reviews-uniview3" {
  bucket = "places-reviews-uniview3"  # Replace with a globally unique bucket name

  acl = "private"  # Access control for the bucket (private, public-read, public-read-write, etc.)
}

 