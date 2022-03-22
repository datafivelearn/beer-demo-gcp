# This is what tells terraform which terraform "provider" to use.  
# A provider is the engine that's building the actual infrastucture based on this definition

# Terraform Version & Backend (statefile) location
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.89.0"
    }
  }
  backend "remote" {
    # Intentionally blank - populated at run time based on the env-config/{env}-backend.conf values
    #organization = ""
    #workspaces {
    #  name = ""
    #}
  }
}

# Terraform Provider
provider "google" {
  project = var.gcp_project_id
  region = var.gcp_region
}
