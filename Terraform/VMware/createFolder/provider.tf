provider "vsphere" {
  user           = var.vc_user
  password       = var.vc_pass
  vsphere_server = var.vc_server

  allow_unverified_ssl = true
}