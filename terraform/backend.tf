terraform {
  backend "gcs" {
    bucket = "terraform-state-bucket-sauter-university-2025"
    prefix = "terraform/state"
  }
}