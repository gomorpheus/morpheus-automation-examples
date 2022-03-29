
resource "aws_s3_bucket" "s3" {
    count = var.bucket_count
    bucket_prefix = var.bucket_prefix
    force_destroy = var.force_destroy
    tags = {
    Date = timestamp()
    mytest = var.mytest
    }
}