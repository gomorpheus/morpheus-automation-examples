# We strongly recommend using the required_providers block to set the
# Azure Provider source and version being used
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 2.65"
    }
  }
}

provider "azurerm" {
  features {}

  subscription_id = var.subscription_id
  client_id       = var.client_id
  client_secret   = var.client_secret
  tenant_id       = var.tenant_id
}

data "azurerm_resource_group" "selected-rg" {
  name = var.resourceGroup
}

data "azurerm_virtual_network" "selected-network" {
  name                = var.virtualNetwork
  resource_group_name = var.resourceGroup
}

data "azurerm_subnet" "selected-subnet" {
  name                 = var.subnet
  virtual_network_name = data.azurerm_virtual_network.selected-network.name
  resource_group_name  = var.resourceGroup
}

resource "azurerm_app_service_environment_v3" "ase-v3" {
  name                = local.basename
  resource_group_name = data.azurerm_resource_group.selected-rg.name
  subnet_id           = data.azurerm_subnet.selected-subnet.id

  internal_load_balancing_mode = "Web, Publishing"

  zone_redundant = var.isZoneRedundant

  cluster_setting {
    name  = "DisableTls1.0"
    value = "1"
  }
}

output "subnetName" {
  value       = data.azurerm_subnet.selected-subnet.name

}

output "subnetId" {
  value       = data.azurerm_subnet.selected-subnet.id

}

