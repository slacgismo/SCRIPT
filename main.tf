provider "aws" {
  region = var.region
}

resource "aws_s3_bucket" "script_raw_bucket" {
  bucket = var.raw_data_bucket_name
}

resource "aws_s3_bucket" "script_clean_bucket" {
  bucket = var.cleaned_data_bucket_name
}

resource "aws_default_vpc" "default" {
  tags = {
    Name = "Default VPC"
  }
}

resource "aws_security_group" "sg" {
  name = "script-postgresql-db-sg"
  vpc_id = "${aws_default_vpc.default.id}"

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 5432
    to_port = 5432
    protocol = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"

    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "script_algorithm_ins" {
  ami                         = "ami-04b9e92b5572fa0d1"
  instance_type               = "t2.medium"
  vpc_security_group_ids      = ["${aws_security_group.sg.id}"]
  associate_public_ip_address = true
  key_name                    = "script"
  #iam_instance_profile        = "${aws_iam_instance_profile.ec2_profile.name}"

  provisioner "file" {
    source      = "../SCRIPT"
    destination = "/home/ubuntu"
    connection {
      type        = "ssh"
      user        = "ubuntu"
      host        = "${self.public_dns}"
      private_key = "${file("script.pem.txt")}"
    }
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt update",
      "sudo apt install -y gcc",
      "sudo apt install -y python3",
      "sudo apt install -y python3-pip",
      "sudo apt-get install -y python3-venv",
      "sudo apt-get install -y python-dev",
      "sudo apt-get install -y libpq-dev python-dev",
      "pip3 install awscli --force-reinstall --upgrade",
      "mkdir ~/mosek",
      "cp ~/SCRIPT/mosek.lic ~/mosek/mosek.lic",
      "sudo sh -c '/bin/echo 1 > /proc/sys/vm/overcommit_memory'",
      "aws configure set aws_access_key_id <>",
      "aws configure set aws_secret_access_key <>",
      "aws configure set default.region us-east-1",
      "pip3 install pandas",
      "pip3 install boto3",
      "pip3 install cvxpy",
      "pip3 install s3fs",
      "pip3 install sklearn",
      "pip3 install psycopg2",
      "pip3 install -f https://download.mosek.com/stable/wheel/index.html Mosek",
      "pip3 install paramiko"
      "pip3 install pip3 install matplotlib"
    ]
    connection {
      type        = "ssh"
      user        = "ubuntu"
      host        = "${self.public_dns}"
      private_key = "${file("script.pem.txt")}"
    }
  }
}

resource "aws_db_instance" "script_postgresql_db" {
  identifier             = "script-postgresql-db"
  allocated_storage      = 20
  storage_type           = "gp2"
  engine                 = "postgres"
  engine_version         = "11.5"
  instance_class         = var.db_instance
  name                   = var.db_name
  username               = var.db_username
  password               = var.db_pwd
  port                   = var.db_port
  publicly_accessible    = true
  vpc_security_group_ids = ["${aws_security_group.sg.id}"]
  skip_final_snapshot    = true
}

output "script_postgresql_db_name" {
  value = "${aws_db_instance.script_postgresql_db.name}"
}

output "script_postgresql_db_host" {
  value = "${aws_db_instance.script_postgresql_db.endpoint}"
}

output "script_postgresql_db_port" {
  value = "${aws_db_instance.script_postgresql_db.port}"
}

output "script_postgresql_db_username" {
  value = "${aws_db_instance.script_postgresql_db.username}"
}

output "script_algorithm_ins_ip" {
  value = "${aws_instance.script_algorithm_ins.public_ip}"
}

output "script_algorithm_ins_dns" {
  value = "${aws_instance.script_algorithm_ins.public_dns}"
}