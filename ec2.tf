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

resource "aws_instance" "uniview_project" {
  ami                    = var.ami_id
  instance_type          = "t2.micro"
  security_groups        = [aws_security_group.uniview_project_sg.name]
  iam_instance_profile   = aws_iam_instance_profile.ec2_s3_profile.name
  user_data              = file("user_data.sh")
  key_name               = "Your_identity_key"

  tags = {
    Name = "Uniview-project"
  }
}

