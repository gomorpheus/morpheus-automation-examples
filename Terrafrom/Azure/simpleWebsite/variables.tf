variable "subscription_id" {}

variable "client_id" {}

variable "client_secret" {}

variable "tenant_id" {}

variable "region" {
   default = "eastus"
}

variable "name_prefix" {
   description = "Name prefix for both Resource Group and Storage Account Creation" 
}


