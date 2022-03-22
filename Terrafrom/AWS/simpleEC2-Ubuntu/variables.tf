variable "access_key" {}
variable "secret_key" {}
variable "region" {
   default = "us-east-1"
}
variable "vpc" {
   default = "vpc-d4c954ae"
}

variable "ami" {
   default = "ami-033b95fb8079dc481"
}
variable "subnet" {
   default = "subnet-b0f7e6fa"
}

variable "itype" {
   default = "t3.micro"
}

variable "secgroupname" {
   default = "IAC-Sec-Group"
}
