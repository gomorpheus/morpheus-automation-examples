output "fqdn" {
  description = "FQDN of the record created"
  value       = aws_route53_record.morpheusR53.fqdn
}