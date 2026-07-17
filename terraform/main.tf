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
  default     = "learn-magic-project"
}

variable "region" {
  type        = string
  description = "The region to deploy resources in"
  default     = "us-central1"
}

# Secret Manager secret for GEMINI_API_KEY
resource "google_secret_manager_secret" "gemini_api_key" {
  secret_id = "gemini-api-key"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "gemini_api_key_version" {
  secret      = google_secret_manager_secret.gemini_api_key.id
  secret_data = "dummy-value-update-manually"
}

# Example Cloud Run Service deployment for the Agent
resource "google_cloud_run_v2_service" "agent_service" {
  name     = "learn-magic-agent"
  location = var.region
  
  template {
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello" # Placeholder image
      env {
        name  = "GOOGLE_CLOUD_PROJECT"
        value = var.project_id
      }
      # Inject secret directly as an env var
      env {
        name = "GEMINI_API_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.gemini_api_key.secret_id
            version = "latest"
          }
        }
      }
    }
  }
}
