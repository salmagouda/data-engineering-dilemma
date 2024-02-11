terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.13.0"
    }
  }
}

provider "google" {
  credentials = var.gcp_key
  project     = var.project
  region      = var.region
}

resource "google_storage_bucket" "de-bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
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


resource "google_bigquery_dataset" "de_dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location

}