terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
  project = "project-d298a763-cbfb-48f5-8c9"
  region  = "us-central1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "project-d298a763-cbfb-48f5-8c9-bucket"
  location      = "US"
  force_destroy = true
  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}