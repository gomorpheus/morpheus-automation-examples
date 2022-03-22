resource "google_storage_bucket" "storage_bucket" {
  name     = var.bucket_name
  location = var.region
}