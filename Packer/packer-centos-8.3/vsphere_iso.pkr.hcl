source "vsphere-iso" "centos" {
    vcenter_server = "${var.remote_host}"
    username = "${var.remote_username}"
    password = "${var.remote_password}"
    insecure_connection = true
    host = "${var.esx_host}"
    datastore = "${var.remote_datastore}"
    // datacenter
    CPUs = "${var.cpus}"
    RAM = "${var.memory}"
    RAM_hot_plug = "${var.ram_hot_plug}"
    video_ram = "${var.video_ram}"
    shutdown_command = "${var.shutdown_command}"
    iso_url = "${var.iso_url}"
    iso_checksum = "${var.iso_checksum}"
    cd_files = "${var.cd_files}"
    cd_label = "${var.cd_label}"
    vm_version = 11
    vm_name = "${var.vm_name}"
    remove_cdrom = true
    guest_os_type = "${var.guest_os_type}"
    boot_command = ["${var.boot_command}"]
    // http_directory = "${var.http_directory}"
    network_adapters {
        network = "${var.vm_network}"
        network_card = "${var.vm_network_card_type}"
    }
    storage {
        disk_size = "${var.disk_size}"
        disk_thin_provisioned = true
    }
    
    ssh_username = "${var.ssh_username}"
    ssh_password = "${var.ssh_password}"
    ssh_wait_timeout = "${var.ssh_wait_timeout}"
    convert_to_template = "${var.convert_to_template}"
    export {
        force = true
        output_directory = "${var.packer_output_directory}"
    }
}