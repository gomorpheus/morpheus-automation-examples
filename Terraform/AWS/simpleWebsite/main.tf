resource "aws_s3_bucket" "web" {
  bucket_prefix = var.bucket_prefix
  force_destroy = true
}

resource "aws_s3_bucket_website_configuration" "web" {
  bucket = aws_s3_bucket.web.bucket

  index_document {
    suffix = "index.html"
  }
}



resource "aws_s3_bucket_acl" "acl" {
  bucket = aws_s3_bucket.web.id
  acl    = "private"
}

resource "aws_s3_object" "index" {
  bucket      = aws_s3_bucket.web.id
  key         = "index.html"
  source      = "files/index.html"
  content_type = "text/html" 
  acl         = "public-read"
}

resource "aws_s3_object" "image" {
  bucket      = aws_s3_bucket.web.id
  key         = "morpheus.png"
  source      = "files/morpheus.png"
  acl         = "public-read"
}