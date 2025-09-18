resource "google_cloud_run_service" "cloudrun" {
    name     = var.service_name
    location = var.region
    
    template {
        spec {
        containers {
            image = var.image_url
        }
        }
    }
    
    traffic {
        percent         = 100
        latest_revision = true
    }
    
    autogenerate_revision_name = true
}