module "S3" {
   source = "./modules/simpleS3"
   bucket_prefix = var.bucket_prefix
   acl_value = var.acl_value
   force_destroy = var.force_destroy
}