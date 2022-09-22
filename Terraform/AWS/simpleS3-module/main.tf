module "S3" {
   source = ".../modules/AWS/simpleS3"
   bucket_prefix = var.bucket_prefix
   force_destroy = var.force_destroy
}
