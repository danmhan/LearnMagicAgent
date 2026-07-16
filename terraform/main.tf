terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" {
  type        = string
  description = "The Google Cloud Project ID"
}

variable "region" {
  type        = string
  description = "The region to deploy resources in"
  default     = "us-central1"
}

# Example Secret Manager secret for GEMINI_API_KEY
resource "google_secret_manager_secret" "gemini_api_key" {
  secret_id = "gemini-api-key"
  replication {
    auto {}
  }
}

# In a real deployment, we would also provision a Cloud Run service 
# or a Vertex AI agent builder endpoint here.
