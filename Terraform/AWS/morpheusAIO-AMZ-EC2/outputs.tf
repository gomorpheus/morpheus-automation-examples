output "morpheus_address" {
  description = "Morpheus public URL"
  value       = "https://${aws_instance.morpheus.public_dns}"
}
