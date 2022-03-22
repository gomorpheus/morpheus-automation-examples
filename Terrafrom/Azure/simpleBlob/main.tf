locals {
  name = lower("${var.name_prefix}${random_id.name.dec}")
}

resource "random_id" "name" {
  byte_length = 6
}

resource "azurerm_resource_group" "resourceGroup" {
  name     = local.name
  location = var.region
}

resource "azurerm_storage_account" "storageAccount" {
  name                     = local.name
  resource_group_name      = azurerm_resource_group.resourceGroup.name
  location                 = azurerm_resource_group.resourceGroup.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "storageContainer" {
  name                  = local.name
  storage_account_name  = azurerm_storage_account.storageAccount.name
  container_access_type = "private"
}

resource "azurerm_storage_blob" "storageBlob" {
  name                   = "morpheus.png"
  storage_account_name   = azurerm_storage_account.storageAccount.name
  storage_container_name = azurerm_storage_container.storageContainer.name
  type                   = "Block"
  source                 = "files/morpheus.png"
}