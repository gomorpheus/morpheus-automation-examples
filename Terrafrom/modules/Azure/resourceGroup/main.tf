resource "azurerm_resource_group" "rg" {
  name     = var.resourceGroup
  location = var.region
}