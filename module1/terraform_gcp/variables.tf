variable "gcp_key" {
  description = "My json key credentials"
  default     = "./keys/my-creds.json"
}

variable "project" {
  description = "My project"
  default     = "ny-rides-sal"
}


variable "location" {
  description = "My project location"
  default     = "me-west1"
}

variable "region" {
  description = "My project region"
  default     = "me-west1"
}


variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "de_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "ny-rides-sal-de-bucket"
}


variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}



