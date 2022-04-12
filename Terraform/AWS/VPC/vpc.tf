variable "vpc_cidr" {
  type        = string
  description = "CIDR for the the VPC"
  default = "172.16.0.0/24"
}

variable "vpc_name" {
  type        = string
  description = "Name for the VPC"
  default = "durka"
}

resource "aws_vpc" "main" {
    cidr_block = var.vpc_cidr

 tags = merge(
    local.default_tags,
    {
      Name = var.vpc_name
    }
  )
}

output "aws_vpc" {
  value = aws_vpc.main
  sensitive = true
}