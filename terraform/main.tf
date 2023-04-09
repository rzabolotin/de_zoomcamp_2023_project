terraform {
  required_version = ">= 1.0"
  backend "local" {}  # Can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
  required_providers {
    google = {
      source  = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.PROJECT_ID
  region = var.REGION
  // credentials = file(var.credentials)  # Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}

## Data Lake
resource "google_storage_bucket" "data-lake-bucket" {
  name          = var.DATA_LAKE_BUCKET_NAME
  location      = var.REGION

  # Optional, but recommended settings:
  storage_class = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  // days
    }
  }

  force_destroy = true
}

# Data Warehouse
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.BQ_STAGE_DATASET
  project    = var.PROJECT_ID
  location   = var.REGION
}

resource "google_bigquery_dataset" "dataset_prod" {
  dataset_id = var.BQ_PROD_DATASET
  project    = var.PROJECT_ID
  location   = var.REGION
}