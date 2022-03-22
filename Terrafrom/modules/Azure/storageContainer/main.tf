resource "azurerm_storage_container" "storageBlob" {
  name                  = var.blob
  storage_account_name  = var.saname
  container_access_type = "private"
}

resource "azurerm_storage_queue" "storageQueue" {
  name                 = var.queuename
  storage_account_name = var.saname
}