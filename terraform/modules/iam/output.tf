output "cloudrun_service_account_email" {
  description = "Email SA Cloud Run"
  value       = google_service_account.cloudrun_sa.email
}

output "github_service_account_email" {
  description = "Email SA GitHub Actions"
  value       = google_service_account.github_sa.email
}