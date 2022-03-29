locals {
  name = lower("${var.name_prefix}${random_id.name.dec}")
}


resource "random_id" "name" {
  byte_length = 6
}


#Create Resource Group
resource "azurerm_resource_group" "resourceGroup" {
  name     = local.name
  location = var.region
}
 
#Create Storage account
resource "azurerm_storage_account" "storageAccount" {
  name                = local.name
  resource_group_name = azurerm_resource_group.resourceGroup.name
 
  location                 = var.region
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
 
  static_website {
    index_document = "index.html"
  }
}
 
#Add index.html to blob storage
resource "azurerm_storage_blob" "index" {
  name                   = "index.html"
  storage_account_name   = azurerm_storage_account.storageAccount.name
  storage_container_name = "$web"
  type                   = "Block"
  content_type           = "text/html"
  source                 = "files/index.html"
}

#Add image to blob storage
resource "azurerm_storage_blob" "image" {
  name                   = "morpheus.png"
  storage_account_name   = azurerm_storage_account.storageAccount.name
  storage_container_name = "$web"
  type                   = "Block"
  source                 = "files/morpheus.png"
}