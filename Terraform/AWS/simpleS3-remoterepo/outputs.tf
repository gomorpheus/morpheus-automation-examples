output "arn" {
  description = "ARN of the bucket"
  value       = module.S3.arn
}

output "name" {
  description = "Name (id) of the bucket"
  value       = module.S3.name
}

output "domainname" {
  description = "Domain Name of the bucket"
  value       = module.S3.domainname
}


