module "createFolder" {
   #source = "../../modules/VMware/createFolder"
   source = "git::https://github.com/gomorpheus/morpheus-automation-examples.git"
   folder_name = var.folder_name
}