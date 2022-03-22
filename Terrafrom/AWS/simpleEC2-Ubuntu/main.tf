resource "aws_security_group" "project-iac-sg" {
  name = var.secgroupname
  vpc_id = var.vpc

  // To Allow SSH Transport
  ingress {
    from_port = 22
    protocol = "tcp"
    to_port = 22
    cidr_blocks = ["0.0.0.0/0"]
  }

  // To Allow Port 80 Transport
  ingress {
    from_port = 80
    protocol = "tcp"
    to_port = 80
    cidr_blocks = ["0.0.0.0/0"]
  }

  // To Allow Port 443 Transport
  ingress {
    from_port = 443
    protocol = "tcp"
    to_port = 443
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
  }

  lifecycle {
    create_before_destroy = true
  }
}


resource "aws_instance" "project-iac" {
  ami = var.ami
  instance_type = var.itype
  subnet_id = var.subnet
  associate_public_ip_address = "true"
  user_data                   = <<EOF
#!/bin/bash -xe
sudo yum update
sudo yum upgrade -y
sudo hostnamectl set-hostname testing.boyd.local
EOF

  vpc_security_group_ids = [
    aws_security_group.project-iac-sg.id
  ]
  root_block_device {
    delete_on_termination = true
    volume_size = 50
  }
  tags = {
      Name = "test001992"
  }


  depends_on = [ aws_security_group.project-iac-sg ]
}
