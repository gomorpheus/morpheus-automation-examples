output "rgid" {
  value = module.azurerm_resource_group.rg.id
}

output "rgname" {
  value = module.rg.name
}

output "rglocation" {
  value = module.rg.location
}

output "storageAccountName" {
  description = "Storage Account Name"
  value       = module.storageAccount.name
}