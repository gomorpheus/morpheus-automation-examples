output "storage_blob_name" {
  description = "The Storarage Blob name"
  value       = azurerm_storage_container.storageContainer.name
}
