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

# variable apis

variable "apis" {
  type        = list(string)
  default     = ["artifactregistry.googleapis.com", "cloudrun.googleapis.com"]
  
}


