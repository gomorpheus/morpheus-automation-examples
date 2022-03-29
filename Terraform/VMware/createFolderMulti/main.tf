data "vsphere_datacenter" "dc" {}

resource "vsphere_folder" "folder" {
  path          = var.folder_name
  type          = "vm"
  datacenter_id = "${data.vsphere_datacenter.dc.id}"
}