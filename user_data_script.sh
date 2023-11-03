#!/bin/bash

# Update and install dependencies
yum update -y
yum install -y python3
pip3 install boto3 sklearn ...

# Copy the analyze_reviews.py from S3 to the EC2 instance
aws s3 cp s3://uniview-scripts/analyze_reviews.py /home/ec2-user/

# Run the script
python3 /home/ec2-user/analyze_reviews.py

