
locals {
  bucket_prefix = "${var.bucket_prefix}${random_id.name.dec}"
}


resource "random_id" "name" {
  byte_length = 6
}



resource "google_storage_bucket" "web" {
  name          = local.bucket_prefix
  location      = var.region

  website {
    main_page_suffix = "index.html"
  }
}

resource "google_storage_default_object_acl" "acl" {
  bucket      = google_storage_bucket.web.name
  role_entity = ["READER:allUsers"]
}

resource "google_storage_bucket_object" "index" {
  name   = "index.html"
  source = "files/index.html"
  bucket = google_storage_bucket.web.name
  content_type = "text/html"
}

resource "google_storage_bucket_object" "image" {
  name   = "morpheus.png"
  source = "files/morpheus.png"
  bucket = google_storage_bucket.web.name
}

resource "google_storage_object_access_control" "index" {
  object = google_storage_bucket_object.index.output_name
  bucket = google_storage_bucket.web.name
  role   = "READER"
  entity = "allUsers"
}

resource "google_storage_object_access_control" "image" {
  object = google_storage_bucket_object.image.output_name
  bucket = google_storage_bucket.web.name
  role   = "READER"
  entity = "allUsers"
}