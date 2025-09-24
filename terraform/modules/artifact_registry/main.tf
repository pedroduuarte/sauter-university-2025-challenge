resource "google_artifact_registry_repository" "repository" {
  format         = var.format
  location       = var.location
  repository_id  = var.repository_id
  description    = var.description
  labels         = var.labels
}