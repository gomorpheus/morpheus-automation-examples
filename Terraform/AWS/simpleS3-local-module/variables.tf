variable "access_key" {}
variable "secret_key" {}
variable "region" {
   default = "us-east-1"
}
variable "bucket_prefix" {}
variable "acl_value" {
   default = "private"
}
variable "force_destroy" {
    type = bool   
    default = false
}
