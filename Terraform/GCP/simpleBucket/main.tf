module "storage_bucket" {
   source = "../../modules/GCP/storageBucket"
   bucket_name = var.bucket_name
   region = var.region
}