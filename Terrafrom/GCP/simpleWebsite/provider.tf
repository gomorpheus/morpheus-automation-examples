provider "google" {
  credentials = var.gcp_auth
  region      = var.region
  project     = "test-310000"
 }