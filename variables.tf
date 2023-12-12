variable "region" {
  description = "AWS region"
  default     = "us-east-2"
}

variable "ami_id" {
  description = "AMI ID for EC2 instance"
  type        = string
}

variable "github_oauth_token" {
  description = "GitHub OAuth token for AWS Amplify"
  type        = string
}

variable "github_repo_url" {
  description = "URL of the GitHub repository for AWS Amplify"
  type        = string
}

variable "key_name" {
  description = "Key name for EC2 instance"
  type  =string
}
