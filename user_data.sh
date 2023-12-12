#!/bin/bash

yum update -y
yum install -y python3
pip3 install boto3 pandas sklearn numpy

aws s3 cp s3://uniview-scripts/analyze_reviews.py /home/ec2-user/
aws s3 cp s3://uniview-scripts/s3tocsv.py /home/ec2-user/
aws s3 cp s3://uniview-scripts/csvtodynamo.py /home/ec2-user/

python3 /home/ec2-user/analyze_reviews.py
python3 /home/ec2-user/s3tocsv.py
python3 /home/ec2-user/csvtodynamo.py 
