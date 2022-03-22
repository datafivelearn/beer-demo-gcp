# These are the variables that are passed into the terraform application at run time from the deployment pipeline

variable "gcp_project_id" {
  type        = string
  description = "The Google Cloud Project Id"
}

variable "gcp_region" {
  type    = string
  #default = "europe-west2"
  description = "The Google Cloud region"
}

variable "env" {
  type    = string
  description = "Environment being deployed to"
}