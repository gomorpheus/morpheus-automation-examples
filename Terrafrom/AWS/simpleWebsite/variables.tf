variable "access_key" {
    type         = string
    description  = "AWS Accesss Key"
}
variable "secret_key" {
    type         = string
    description  = "AWS Secret Key"
}
variable "region" {
    type         = string
    description  = "AWS Region"
    default = "us-east-1"
}
variable "bucket_prefix" {
    type         = string
    description  = "Bucket Prefix - A random string will be added to the end of this prefix"
}
