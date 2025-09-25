variable "dataset_id" {
  description = "The ID of the dataset to create."
  type        = string
  
}

variable "friendly_name" {
  description = "A descriptive name for the dataset."
  type        = string
}

variable "description" {
  description = "A user-friendly description of the dataset."
  type        = string
}

variable "location-big-query" {
  description = "The geographic location where the dataset should reside."
  type        = string
  default     = ""
}

variable "default_table_expiration_ms" {
  description = "The default lifetime of all tables in the dataset."
  type        = number
}

variable "labels" {
  description = "A set of key/value label pairs to assign to the dataset."
  type        = map(string)
}

variable "table_id" {
  description = "The ID of the table to create."
  type        = string
}


  
variable "source_format" {
  description = "The format of the external data source."
  type        = string
}

variable "source_uris" {
  description = "The URIs of the external data source."
  type        = list(string)
}



