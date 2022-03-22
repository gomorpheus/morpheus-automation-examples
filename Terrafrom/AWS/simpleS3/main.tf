resource "aws_s3_bucket" "s3" {
    bucket_prefix = var.bucket_prefix
    force_destroy = var.force_destroy
    tags = {
    Name = var.bucket_prefix
    Date = timestamp()
    }
}

resource "aws_s3_bucket_acl" "acl" {
  bucket = aws_s3_bucket.s3.id
  acl    = var.acl_value
}