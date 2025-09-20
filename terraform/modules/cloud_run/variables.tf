variable "service_name" {
    description = "The name of the Cloud Run service."
    type        = string
  
}

variable "region" {
    description = "The region where the Cloud Run service will be deployed."
    type        = string
    default     = "us-central1"
}

variable "image_url" {
    description = "The URL of the container image to deploy."
    type        = string
}

