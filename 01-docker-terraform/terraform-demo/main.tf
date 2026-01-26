terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
  project     = "turnkey-light-485419-q0"
  region      = "us-central1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "turnkey-light-485419-q0-terra-bucket"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}