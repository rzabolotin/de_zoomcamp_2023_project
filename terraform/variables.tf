
variable "PROJECT_ID" {
  description = "Your GCP Project ID"
  type = string
}

variable "REGION" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  type = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}

variable "DATA_LAKE_BUCKET_NAME" {
  description = "Name of data-lake bucket to be created"
  type = string
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
}