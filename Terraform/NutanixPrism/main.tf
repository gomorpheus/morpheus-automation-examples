# terraform {
#   required_providers {
#     nutanix = {
#       source  = "nutanix/nutanix"
#       version = "1.8.1"
#     }
#   }
# }
# set provider, Nutanix 
provider "nutanix" {
  username     = var.nutanix_username
  password     = var.nutanix_password
  endpoint     = var.nutanix_endpoint
  insecure     = true
  wait_timeout = 60
  port         = 9440
}

# Get Cluster 
data "nutanix_cluster" "cluster" {
  name = var.nutanix_cluster
}

# Get subnets
data "nutanix_subnet" "subnet" {
  subnet_name = var.subnet_name
}

# Get Image info
data "nutanix_image" "image" {
  image_name = var.nutanix_imagename
}

# unattend.xml template
data "template_file" "unattend" {
  template = file("${path.module}/unattend.xml")
  vars = {
    vm_name             = var.t_vm_name
    hostname            = var.t_hostname
    admin_username      = var.t_admin_username
    admin_password      = var.t_admin_password
  }
}

resource "nutanix_virtual_machine" "vm" {
  #  count                = 1
  name                 = var.t_vm_name
  description          = var.t_vm_description
  provider             = nutanix
  cluster_uuid         = data.nutanix_cluster.cluster.id
  num_vcpus_per_socket = var.t_num_vcpus_per_socket
  num_sockets          = var.t_num_sockets
  memory_size_mib      = var.t_memory_size_mib
  boot_type            = var.t_boot_type

  # Set NIC
  nic_list {
    subnet_uuid = data.nutanix_subnet.subnet.id
  }

  # Unattend.xml 
  guest_customization_sysprep = {
    install_type = "PREPARED"
    unattend_xml = base64encode(data.template_file.unattend.rendered)
  }

  # image reference
  disk_list {
    data_source_reference = {
      kind = "image"
      uuid = data.nutanix_image.image.id
    }
  }

  # disk info
  disk_list {
    #disk_size_bytes = 40 * 1024 * 1024 * 1024
    disk_size_bytes = var.t_disk_2_size
    device_properties {
      device_type = "DISK"
      disk_address = {
        "adapter_type" = "SCSI"
        "device_index" = "1"
      }
    }
  }
}


# output "VMID" {
#   value = nutanix_virtual_machine.vm
# }
#
#
#output "ip_address" {
#  value = nutanix_virtual_machine.vm.nic_list_status.0.ip_endpoint_list[0]["ip"]
#}
