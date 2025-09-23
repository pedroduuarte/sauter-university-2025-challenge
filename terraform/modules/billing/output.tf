# terraform/modules/billing/outputs.tf

output "budget_id" {
  description = "Budget ID."
  value       = google_billing_budget.budget.id
}

output "notification_channel_names" {
  description = "Map of emails to the names of notification channels."
  value = {
    for email, channel in google_monitoring_notification_channel.email_channel :
    email => channel.name
  }
}