variable "subscription_id" {
    type = string
    sensitive = true
    #default = "<%= customOptions.azurergprep_subscriptionid %>"
}
variable "client_id" {
    type = string
    sensitive = true
    #default = "<%= customOptions.azurergprep_clientid %>"
}
variable "client_secret" {
    type = string
    sensitive = true
    #default = "<%= customOptions.azurergprep_clientsecret %>"
}
variable "tenant_id" {
    type = string
    sensitive = true
    #default = "<%= customOptions.azurergprep_tenantid %>"
}

variable "resourceGroup" {
  description = "Resource Group"
  type        = string
  #default     = "terratest"
}

variable "virtualNetwork" {
  description = "Virtual Network"
  #type        = string
}

variable "subnet" {
  description = "Subnet"
  #type        = string
}

variable "system" {
  type        = string
  description = "customer system name"
  #default = "<%= customOptions.global_system.tokenize(':')[0] %>"
}

variable "environment" {
  type        = string
  description = "customer environment to deploy"
  #default = "<%= customOptions.global_environment.tokenize(':')[1] %>"
}

variable "isZoneRedundant" {
  description = "Deploy App Service Environment with availability zones supported"
  type        = bool
}

variable "customIdentifier" {
  type        = string
  description = "Custom identifier will be added to the ASE name"
  #default = "<%= customOptions.global_system.tokenize(':')[0] %>"
}

locals {
  basename = lower("${var.system}-${var.environment}-${var.customIdentifier}-ase")
}