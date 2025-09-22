variable "project_id" {
  description = "The ID of the project in which to create the Artifact Registry repository."
  type        = string
  
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

# variable big_query

variable "dataset_id" {
  description = "The ID of the dataset to create."
  type        = string
  default = "reservatorios_externos_dataset"
}

variable "friendly_name" {
  description = "A descriptive name for the dataset."
  type        = string
  default     = "test"
}

variable "location-big-query" {
  description = "The geographic location where the dataset should reside."
  type        = string
  default     = "US"
  
}

variable "default_table_expiration_ms" {
  description = "The default lifetime of all tables in the dataset, in milliseconds."
  type        = number
  default     = null
}


variable "table_id" {
  description = "The ID of the table to create."
  type        = string
  default     = "reservatorios_externos"
}


  
variable "source_format" {
  description = "The format of the external data source."
  type        = string
  default     = "PARQUET"
}

variable "source_uris" {
  description = "The URIs of the external data source."
  type        = list(string)
  default     = ["gs://sauter-bucket-2025/raw/*.parquet"]
  
}

# variable iam

variable "cloudrun_sa_name" {
  type        = string
  default     = "cloudrun-sa"
  description = "Nome da service account para o Cloud Run"
}

variable "github_sa_name" {
  type        = string
  default     = "github-actions-sa"
  description = "Nome da service account para o GitHub Actions"
}