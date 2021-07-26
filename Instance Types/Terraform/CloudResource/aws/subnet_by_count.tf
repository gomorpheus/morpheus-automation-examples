# This spec template creates AWS subnets based on the count requested utilizing the vpc cidr provided in var.vpc_cidr variable

locals {
  bitCount = sum([tonumber(local.subnet_options.cidrMask),-tonumber(split("/",var.vpc_cidr)[1])])
}

resource "aws_subnet" "main" {
    count = tonumber(var.subnetCount)
    vpc_id     = aws_vpc.main.id
    cidr_block = cidrsubnet(var.vpc_cidr, local.bitCount, count.index)

    tags = merge(
        local.default_tags,
        {
        Name = "${var.vpc_name}-subnet-0${count.index}"
        }
    )
}

output "aws_subnet" {
  value = aws_subnet.main
  sensitive = true
}