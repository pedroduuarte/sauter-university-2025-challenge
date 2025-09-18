variable "apis" {
  type        = list(string)
  default     = []
  
}

variable "project_id" {
  description = "The ID of the project in which to enable the APIs."
  type        = string
  
}