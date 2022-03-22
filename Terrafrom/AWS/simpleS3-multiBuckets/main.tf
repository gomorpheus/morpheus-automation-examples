resource "aws_s3_bucket" "s3" {
    for_each = toset(var.bucket_prefix)
    bucket_prefix = each.value
    force_destroy = var.force_destroy
    tags = {
    Name = each.value
    Date = timestamp()
    }
}

resource "aws_s3_bucket_acl" "acl" {
  for_each = toset(var.bucket_prefix)
  bucket = aws_s3_bucket.s3[each.key].id
  acl    = var.acl_value
}