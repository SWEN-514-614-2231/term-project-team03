output "ec2_public_ip" {
  value = aws_instance.uniview_project.public_ip
  description = "The public IP of the Uniview EC2 instance"
}

