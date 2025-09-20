module "artifact_registry" {
  source        = "./modules/artifact_registry"
  format        = var.format
  location      = var.region
  repository_id = var.repository_id
  description   = var.description
  labels        = var.labels

}

module "cloudrun" {
  source       = "./modules/cloud_run"
  service_name = var.service_name
  region       = var.region
  image_url    = var.image_url
}

module "bucket" {
  source      = "./modules/bucket"
  bucket_name = var.bucket_name
  location    = var.location
  labels      = { environment = "dev", team = "sauter" }
}