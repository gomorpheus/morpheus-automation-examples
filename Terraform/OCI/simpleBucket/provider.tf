provider "oci" {
   tenancy_ocid = var.tenancy
   user_ocid = var.user
   fingerprint = var.fingerprint
   private_key = var.key
   region = var.region
}