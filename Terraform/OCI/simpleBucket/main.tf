module "OCIbucket" {
   source = "../../modules/OCI/simpleBucket"
   bucket_name = var.bucket_name
   compartment = var.compartment
   namespace = var.namespace
   
}