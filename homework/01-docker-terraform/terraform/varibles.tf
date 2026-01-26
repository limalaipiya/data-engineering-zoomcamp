variable "credentials" {
  description = "My Credentials"
  default     = "C:/data-engineering-zoomcamp/homework/01-docker-terraform/terraform/keys/my-creds.json"
}

variable "project" {
  description = "Project"
  default     = "cogent-tangent-485513-u5"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "location" {
  description = "Project location"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dtaset name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "Bucket name"
  default     = "cogent-tangent-485513-u5-terra-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}