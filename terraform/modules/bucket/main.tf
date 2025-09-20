resource "google_storage_bucket" "bucketsauter" {
  name     = var.bucket_name
  location = var.location

  uniform_bucket_level_access = true

  labels = var.labels
}