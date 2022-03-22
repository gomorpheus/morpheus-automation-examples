variable "bucket_prefix" {}
variable "force_destroy" {
    type = bool   
    default = false
}

variable "acl_value" {
   default = "private"
}