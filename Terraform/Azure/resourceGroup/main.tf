module "rg" {
   source = "../../modules/Azure/resourceGroup"
   resourceGroup = var.resourceGroup
   region = var.region
}