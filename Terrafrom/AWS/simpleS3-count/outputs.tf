output "arn" {
  description = "ARN of the bucket"
  value       = aws_s3_bucket.s3[0].arn
}

output "name" {
  description = "Name (id) of the bucket"
  value       = aws_s3_bucket.s3[0].id
}

output "domainname" {
  description = "Domain NAme of Bucket"
  value       = aws_s3_bucket.s3[0].bucket_domain_name
}
