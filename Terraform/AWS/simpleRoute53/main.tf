resource "aws_route53_record" "morpheusR53" {
  zone_id = var.hosted_zone_id
  name    = var.record_name
  type    = "A"
  ttl     = "300"
  records = [var.record_ip]
}