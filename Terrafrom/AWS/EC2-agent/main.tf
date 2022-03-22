resource "aws_security_group" "morpheus_aio_sg" {
  name   = var.sec_group_name
  vpc_id = var.vpc

  // To Allow SSH Transport
  ingress {
    from_port   = 22
    protocol    = "tcp"
    to_port     = 22
    cidr_blocks = ["0.0.0.0/0"]
  }

  // To Allow Port 80 Transport
  ingress {
    from_port   = 80
    protocol    = "tcp"
    to_port     = 80
    cidr_blocks = ["0.0.0.0/0"]
  }

  // To Allow Port 443 Transport
  ingress {
    from_port   = 443
    protocol    = "tcp"
    to_port     = 443
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  lifecycle {
    create_before_destroy = true
  }
}


resource "aws_instance" "morpheus" {
  ami                         = data.aws_ami.amazon2.id
  instance_type               = var.type
  subnet_id                   = data.aws_subnets.subnets.ids[0]
  associate_public_ip_address = "true"
  user_data = <<-EOF
   #cloud-config
   runcmd:
   - <%=instance.cloudConfig.agentInstall%>
   - <%=instance.cloudConfig.finalizeServer%>
   EOF

  vpc_security_group_ids = [aws_security_group.morpheus_aio_sg.id]
  root_block_device {
    delete_on_termination = true
    volume_size           = 50
  }
  tags = {
    Name = var.name
  }


  depends_on = [aws_security_group.morpheus_aio_sg]
}

data "aws_subnets" "subnets" {
  filter {
    name   = "vpc-id"
    values = [var.vpc]
  }
}

data "aws_ami" "amazon2" {
  most_recent = true

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-ebs"]
  }
  owners = ["amazon"]
}

