resource "oci_objectstorage_bucket" "bucket" {
     compartment_id = var.compartment
     name           = var.bucket_name
     namespace      = var.namespace
}