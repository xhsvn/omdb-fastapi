# shared variables

variable "gcp_project_id" {
  description = "Project id"
  type        = string
}

variable "gcp_region" {
  description = "Region"
  type        = string
  default     = "europe-west1"
}

variable "gcp_zone" {
  description = "Zone of the components"
  type        = string
  default     = "europe-west1-b"
}


# Application variables

variable "app_name" {
  description = "App name"
  type        = string
  default     = "omdb-brite"
}

variable "worker_subscription_url_path" {
  description = "URL path for worker subscription"
  type        = string
  default     = "/movies/fetch"
}

variable "worker_subscription_dead_letter_url_path" {
  description = "URL path for worker dead letter subscription"
  type        = string
  default     = "/movies/fetch/dlq"
}


# Cloud Run variables

variable "container_image" {
  description = "Container image"
  type        = string
  default     = ""
}

variable "container_command_api" {
  description = "Command to run during the container startup"
  type        = list(string)
  default     = ["./scripts/start_api"]
}

variable "container_command_worker" {
  description = "Command to run during the container startup"
  type        = list(string)
  default     = ["./scripts/start_worker"]
}



variable "omdb_api_key" {
  description = "OMDb API key"
}
