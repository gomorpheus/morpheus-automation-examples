variable "gcp_auth" {
  type = string
  sensitive = true
}

variable "vm_name" {
  type = string 
}

variable "project" {
  type = string
}

variable "region" {
  type = string
}

variable "zone" {
  type = string 
}

variable "username" {
  type = string 
  description = "Specifies the username associated with the SSH key"
}

variable "ssh_key" {
  type = string 
  sensitive = true 
  description = "Specifies the public SSH key that will be added to the virtual machine"
}


