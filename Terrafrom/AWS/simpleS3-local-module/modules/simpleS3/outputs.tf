output "arn" {
  description = "ARN of the bucket"
  value       = aws_s3_bucket.s3.arn
}

output "name" {
  description = "Name (id) of the bucket"
  value       = aws_s3_bucket.s3.id
}

output "domainname" {
  description = "Domain NAme of Bucket"
  value       = aws_s3_bucket.s3.bucket_domain_name
}