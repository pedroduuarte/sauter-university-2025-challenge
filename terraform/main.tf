module "artifact_registry" {
  source        = "./modules/artifact_registry"
  format        = var.format
  location      = var.region
  repository_id = var.repository_id
  description   = var.description
  labels        = var.labels
  depends_on = [ module.project ]

}

#module "cloudrun" {
 # source       = "./modules/cloud_run"
  #service_name = "sauter-cloud-run-service"
  #region       = var.region
  #image_url    = var.image_url
#}

module "project" {
  source     = "./modules/apis"
  project_id = var.project_id
  apis       = var.apis
}