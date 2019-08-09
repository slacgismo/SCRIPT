provider "aws" {
  region = "us-west-2"
}

resource "aws_instance" "script" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.instance.id]

  tags = {
    Name = "script-web-application"
  }
}

resource "aws_security_group" "instance" {
  name = "script-instance"
  ingress {
    from_port   = var.server_port
    to_port     = var.server_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

variable "server_port" {
  description = "The port the server will use for HTTP requests"
  type        = number
  default     = 80
}

output "public_ip" {
  value       = aws_instance.script.public_ip
  description = "The public IP of the SCRIPT web server"
}