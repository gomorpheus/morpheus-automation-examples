resource "google_compute_instance" "my_vm" {
  name         = var.vm_name
  machine_type = "f1-micro"
  zone         = var.zone
  tags         = ["ssh"]
  boot_disk {
    auto_delete = true
    
    initialize_params {
      image = "projects/debian-cloud/global/images/debian-12-bookworm-v20240709"
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }

    metadata = {
      ssh-keys = "${var.username}:${var.ssh_key}"
  }

    metadata_startup_script = <<-EOF
    #!/bin/bash
    <%=instance.cloudConfig.agentInstall%>
    <%=instance.cloudConfig.finalizeServer%>
    EOF
}

resource "google_compute_firewall" "allow-ssh" {
  name    = "allow-ssh"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["ssh"]
}