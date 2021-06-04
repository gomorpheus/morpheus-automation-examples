variable "access_key" {
  type        = string
}

variable "secret_key" {
  type        = string
}

variable "subnetCount" {
  type = number
  default = "<%=customOptions.subnetCount%>"
}

variable "sensitive_thing" {
  type = string
  default = "this_var_is_sensitive"
  sensitive = true
}