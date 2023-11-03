provider "aws"{
 region = "us-east-2"
}

/* Lambda for Fetching Data
resource "aws_lambda_function" "fetch_data" {
  filename      = "./lambda_function.zip"
  function_name = "FetchDataFunction"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"
  source_code_hash = filebase64sha256("./lambda_function.zip")
}
*/

# Lambda for Data Preprocessing
resource "aws_lambda_function" "data_preprocessing" {
  filename      = "./data_preprocessing.py.zip"
  function_name = "DataPreprocessingFunction"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"
  source_code_hash = filebase64sha256("./data_preprocessing.py.zip")
}

resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
        Effect = "Allow",
        Sid    = ""
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_s3_full_access" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
  role       = aws_iam_role.lambda_exec.name
}

# EC2 Configuration for Sentiment Analysis and Keyword Extraction

resource "aws_security_group" "uniview_project_sg" {
  name        = "uniview-project-sg"
  description = "Allow SSH inbound traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_iam_role" "ec2_s3_role" {
  name = "EC2S3Role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Principal = {
          Service = "ec2.amazonaws.com"
        },
        Effect = "Allow",
        Sid    = ""
      }
    ]
  })
}

resource "aws_iam_instance_profile" "ec2_s3_profile" {
  name = "EC2S3InstanceProfile"
  role = aws_iam_role.ec2_s3_role.name
}

resource "aws_iam_role_policy_attachment" "ec2_s3_policy_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
  role       = aws_iam_role.ec2_s3_role.name
}

resource "aws_instance" "uniview_project" {
  ami           = "ami-01f48e1e4b60cb973" # Replace with your AMI ID
  instance_type = "t2.micro" 

  key_name               = "MZ_AWS_KEY.pem" 
  security_groups        = [aws_security_group.uniview_project_sg.name]
  iam_instance_profile   = aws_iam_instance_profile.ec2_s3_profile.name
  user_data = file("user_data_script.sh")

  tags = {
    Name = "Uniview-project"
  }
}

