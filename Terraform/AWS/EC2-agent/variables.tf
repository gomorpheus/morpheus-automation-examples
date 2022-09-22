variable "access_key" {
  type        = string
  description = "AWS Accesss Key"
}
variable "secret_key" {
  type        = string
  description = "AWS Secret Key"
}
variable "name" {
  type        = string
  description = "This will be the display name of the instance assinged by tag"
}

variable "region" {
  type        = string
  description = "AWS Region"
  default     = "us-east-1"
}
variable "vpc" {
  type        = string
  description = "VPC id required to provision instance. 1st subnet will be chosen from VPC"
  default     = "vpc-a4f961d9"

}

variable "type" {
  type        = string
  description = "AWS type size. Morpheus requires at least 2CPU 8GB Ram"
  default     = "t3.large"

}

variable "sec_group_name" {
  type        = string
  description = "Will create the security group specified and assign to instance"
  default     = "morpheus-aio-sec-group"
}