output "url" {
  description = "The base URL of the bucket, in the format gs://<bucket-name>"
  value       = "https://storage.googleapis.com/${google_storage_bucket.web.name}/index.html"
}

