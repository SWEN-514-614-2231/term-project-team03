variable "region" {
  description = "The AWS region"
  default     = "us-east-2"
}

variable "ami_id" {
  description = "The ID of the AMI to use for the EC2 instance"
  default     = "ami-01f48e1e4b60cb973"  # Replace with your AMI ID
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t2.micro"
}

