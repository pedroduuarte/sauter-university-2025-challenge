variable "bucket_name" {
  description = "The name of the bucket."
  type        = string
  
}

variable "location" {
  description = "The location of the bucket."
  type        = string
  default     = "US"
  
}

variable "labels" {
  type        = map(string)
  default     = {}
}