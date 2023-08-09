terraform {
  required_providers {
    vsphere = {
      source = "hashicorp/vsphere"
      version = ">= 0.14.5"
    }
  }
}
provider "vsphere" {
  user           = var.vc_user
  password       = var.vc_pass
  vsphere_server = var.vc_server
  allow_unverified_ssl = true
}