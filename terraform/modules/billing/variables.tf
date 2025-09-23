variable "billing_account_id" {
  type        = string
  description = "Google Cloud billing account ID."
}

variable "project_id" {
  type        = string
  description = "Project ID."
}


variable "notification_emails" {
  type        = list(string)
  description = "Email list to receive alerts."
}

variable "budget_amount" {
  type        = string
  description = "The budget amount."
}

variable "currency_code" {
  type        = string
  description = "The currency code."
  default     = ""
}

variable "threshold_percentages" {
  type        = list(number)
  description = "List of percentages for alerts."
  default     = []
}