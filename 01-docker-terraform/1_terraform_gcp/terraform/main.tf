terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.32.0"
    }
  }
}

provider "google" {
  project     = var.project
  credentials = file(var.credentials_path)
  region      = var.region
}

resource "google_storage_bucket" "data-lake-bucket" {
  name          = "${var.project}-${var.gcs_bucket_name}"
  location      = var.region
  force_destroy = true
  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
    condition {
      age = 30
    }
  }
}