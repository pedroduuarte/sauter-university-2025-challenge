module "artifact_registry" {
  source        = "./modules/artifact_registry"
  format        = var.format
  location      = var.region
  repository_id = var.repository_id
  labels        = var.labels

}

module "cloudrun" {
  source       = "./modules/cloud_run"
  service_name = var.service_name
  region       = var.region
  image_url    = var.image_url
  service_account_email = module.iam.cloudrun_service_account_email
}

module "bucket" {
  source      = "./modules/bucket"
  bucket_name = var.bucket_name
  location    = var.location
  labels      = var.labels
}

module "big_query" {
  source                       = "./modules/big_query"
  dataset_id                   = var.dataset_id
  description                  = "Dataset for external reservoirs data"
  friendly_name                = var.friendly_name
  location-big-query           = var.location-big-query
  default_table_expiration_ms  = var.default_table_expiration_ms
  labels                       = var.labels
  table_id                     = var.table_id
  source_format                = var.source_format
  source_uris                  = var.source_uris
}

module "iam" {
  source            = "./modules/iam"
  project_id        = var.project_id
  cloudrun_sa_name  = "cloudrun-sa"
  github_sa_name    = "github-actions-sa"
}