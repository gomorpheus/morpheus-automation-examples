output "website_endpoint" {
  value = "http://${aws_s3_bucket_website_configuration.web.website_endpoint}"
}