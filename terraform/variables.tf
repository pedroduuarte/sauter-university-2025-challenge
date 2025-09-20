variable "project_id" {
  description = "The ID of the project in which to create the Artifact Registry repository."
  type        = string
  default = "canvas-provider-472313-n5"
  
}

variable "region" {
  description = "The region in which to create the Artifact Registry repository."
  type        = string
  default     = "us-east1"
}



# variable artifact_registry_repository

variable "location" {
  type        = string
  default = "us-east1"
  
}

variable "repository_id" {
  type        = string
  default = "sauter-projet-repo"
}

variable "description" {
  type        = string
  default     = "repositorio do projeto sauter"
}

variable "labels" {
  type        = map(string)
  default     = {resource = "terraform"}
}

variable "format" {
  type        = string
  default     = "DOCKER"
}

# variable cloud_run

variable "service_name" {
    description = "The name of the Cloud Run service."
    type        = string
    default = "sauter-cloud-run-service"
  
}

variable "image_url" {
    description = "The URL of the container image to deploy."
    type        = string
    default = "us-docker.pkg.dev/cloudrun/container/hello"
}


# variable bucket

variable "bucket_name" {
  description = "The name of the bucket."
  type        = string
  default = "sauter-bucket-2025"
  
}