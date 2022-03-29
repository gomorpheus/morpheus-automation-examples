variable "subscription_id" {}

variable "client_id" {}

variable "client_secret" {}

variable "tenant_id" {}

variable "region" {
   default = "eastus"
}

variable "name_prefix" {
   description = "Name prefix for Resource Group, Storage Account and Container." 
}


