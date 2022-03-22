provider "google" {
  credentials = var.gcp_auth
  region      = "us-central1"
  project     = "test-310000"
 }