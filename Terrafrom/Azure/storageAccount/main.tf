module "rg" {
   source = "../../modules/Azure/resourceGroup"
   resourceGroup = var.rgname
   region = var.rglocation
}

module "storageAccount" {
   source = "../../modules/Azure/storageAccount"
   saname = var.storageAccountName
   rgname = module.rg.name
   rglocation = module.rg.location
}