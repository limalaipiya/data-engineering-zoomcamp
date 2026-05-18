variable "project" {
  description = "Project"
  default     = "project-d298a763-cbfb-48f5-8c9"
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
  default     = "project-d298a763-cbfb-48f5-8c9-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}