provider "google" {
  project     = var.project
  region      = var.region
  zone        = var.zone
  credentials = var.gcp_auth
}