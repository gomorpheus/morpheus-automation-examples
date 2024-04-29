variable "t_vm_description" {
  description = "Nutanix VM description"
  type        = string
  sensitive   = false
}

# variable "t_ipv4_address" {
#   description = "IPv4 van VM"
#   type        = string
#   sensitive   = false
# }

variable "t_vm_name" {
  description = "Nutanix VM name"
  type        = string
  sensitive   = false
}

variable "t_hostname" {
  description = "hostname"
  type        = string
  sensitive   = false
}

variable "subnet_name" {
  description = "NIC VLAN name"
  type        = string
  sensitive   = false
}

variable "nutanix_imagename" {
  description = "Name of image for VM"
  type        = string
  sensitive   = false
}

variable "t_num_vcpus_per_socket" {
  description = "Nutanix VM vCores per socket"
  type        = string
  default     = "1"
}

variable "t_num_sockets" {
  description = "Nutanix VM vCPU's"
  type        = string
}

variable "t_memory_size_mib" {
  description = "Nutanix VM vMEM"
  type        = string
}

variable "t_disk_2_size" {
  description = "Nutanix VM data disk 2"
  type        = number
}

variable "t_boot_type" {
  description = "Nutanix VM Boottype"
  type        = string
  default     = "UEFI"
}


# Windows Authentication
variable "t_admin_username" {
  description = "Admin user"
  type        = string
  sensitive   = true
  default     = "Administrator"
}

variable "t_admin_password" {
  description = "Admin pass"
  type        = string
  sensitive   = true
}

# Nutanix cluster definitie
variable "nutanix_endpoint" {
  description = "Nutanix endpoint"
  type        = string
  sensitive   = false
}

variable "nutanix_cluster" {
  description = "Nutanix Cluster"
  type        = string
  sensitive   = false
}

# redelijk statisch vanaf hier ;-)
variable "nutanix_username" {
  description = "Nutanix user"
  type        = string
  sensitive   = true
}

variable "nutanix_password" {
  description = "Nutanix password"
  type        = string
  sensitive   = true
}


