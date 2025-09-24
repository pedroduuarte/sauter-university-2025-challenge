variable "location" {
  description = "The location of the Artifact Registry repository."
  type        = string
  
}

variable "repository_id" {
  description = "The ID of the Artifact Registry repository."
  type        = string
}

variable "description" {
  description = "The description of the Artifact Registry repository."
  type        = string
  default     = ""
}

variable "labels" {
  description = "Labels to apply to the Artifact Registry repository."
  type        = map(string)
  default     = {}
}

variable "format" {
  description = "The format of packages that are stored in the repository."
  type        = string
  default     = "DOCKER"
}