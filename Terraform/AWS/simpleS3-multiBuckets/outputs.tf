output "arns" {
  value = values(aws_s3_bucket.s3)[*].arn
}

output "names" {
  description = "Name (id) of the bucket"
  value       = values(aws_s3_bucket.s3)[*].id
}

output "domainnames" {
  description = "Domain Name of Bucket"
  value       = values(aws_s3_bucket.s3)[*].bucket_domain_name
}

