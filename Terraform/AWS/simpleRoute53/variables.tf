variable "access_key" {}
variable "secret_key" {}
variable "region" {
    default = "us-east-1"
}
variable "hosted_zone_id" {}
variable "record_name" {
    default = "morpheusR53"
}
variable "record_ip" {}