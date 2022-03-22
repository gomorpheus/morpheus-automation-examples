module "rg" {
   source = "git::https://github.com/rboydmpc/terraformModules.git//Azure/resourceGroup"
   resourceGroup = var.resourceGroup
   region = var.region
}