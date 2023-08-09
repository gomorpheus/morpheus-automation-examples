module "createFolder" {
   #source = "../../modules/VMware/createFolder"
   source = "https://github.com/gomorpheus/morpheus-automation-examples/tree/main/Terraform/modules/VMware/createFolder"
   folder_name = var.folder_name
}