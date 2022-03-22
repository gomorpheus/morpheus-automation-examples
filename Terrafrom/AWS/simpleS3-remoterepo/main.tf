module "S3" {
   source = "git::https://github.com/rboydmpc/terraformModules.git//AWS/simpleS3"
   bucket_name = var.bucket_name
}