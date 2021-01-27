variable "boot_command"  {}
variable "floppy_files"  { default = "null" }
variable "cd_label" { default = "OEMDRV" }
variable "cd_files" {}
variable "http_directory" { default = "null" }
variable "disk_type_id"  {}
variable "guest_os_type" {}
variable "headless" {}
variable "iso_url" {}
variable "iso_checksum" {}
variable "iso_checksum_type" {}
variable "cpus" {}
variable "memory" {}
variable "disk_size" {}
variable "boot_wait" {}
variable "ssh_username" {}
variable "ssh_password" {}
variable "ssh_wait_timeout" {}
variable "shutdown_command" {}
variable "tools_upload_flavor" {}
variable "ram_hot_plug" { default = true }
variable "remote_type" {}
variable "remote_host" {}
variable "remote_username" {}
variable "remote_password" {}
variable "remote_datastore" {}
variable "skip_compaction" {}
variable "keep_registered" {}
variable "format" {}
variable "vnc_disable_password" {}
variable "vmx_data" {}
variable "vm_name" {}
variable "convert_to_template" { default = true }
variable "rhsm_username" { default = "" }
variable "rhsm_password" { default = "" }
variable "rhsm_pool" { default = "" }
variable "packer_output_directory" { default = "packer_output" }
variable "video_ram" { default = "16384" }
variable "vm_network" {}
variable "vm_network_card_type" { default = "vmxnet3" }
variable "esx_host" {}