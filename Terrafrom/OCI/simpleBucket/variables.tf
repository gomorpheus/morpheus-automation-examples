variable "tenancy" { }
variable "user" {}
variable "fingerprint" {}
variable "bucket_name" {}
variable "namespace" {}
variable "compartment" {}
variable "region" {
  default = "us-ashburn-1"
}

variable "key" {
  type = string
}


