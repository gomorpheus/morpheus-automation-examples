build {
  sources = [
    "source.vsphere-iso.centos"
  ]
  provisioner "file" {
    source = "scripts/os_detect.sh"
    destination = "/tmp/os_detect.sh"
  }
  provisioner "shell" {
    script = "scripts/setup.sh"
  }
  provisioner "shell" {
    script = "scripts/cleanup.sh"
  }
}