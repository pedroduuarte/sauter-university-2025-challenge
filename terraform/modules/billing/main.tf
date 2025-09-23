resource "google_monitoring_notification_channel" "email_channel" {
  for_each = toset(var.notification_emails)

  display_name = "budget alert - ${each.key}" 
  type         = "email"
  labels = {
    email_address = each.key
  }
}

resource "google_billing_budget" "budget" {
  billing_account = var.billing_account_id
  display_name    = "Project Budget ${var.project_id} (R$ ${var.budget_amount})"

  budget_filter {
    projects = ["projects/${var.project_id}"]
  }

  amount {
    specified_amount {
      currency_code = var.currency_code
      units         = var.budget_amount
    }
  }

  dynamic "threshold_rules" {
    for_each = toset(var.threshold_percentages)
    content {
      threshold_percent = threshold_rules.value
    }
  }

  all_updates_rule {
    monitoring_notification_channels = [
      for channel in google_monitoring_notification_channel.email_channel : channel.name
    ]
    disable_default_iam_recipients = true
  }
}