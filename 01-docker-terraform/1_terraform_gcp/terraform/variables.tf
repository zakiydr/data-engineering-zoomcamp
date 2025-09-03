variable "credentials_path" {
  description = "Path ke file kunci JSON service account"
  type        = string
}

variable "project" {
  description = "ID proyek Google Cloud"
  type        = string

}

variable "region" {
  description = "Wilayah Google Cloud"
  type        = string
  default     = "asia-southeast2"

}

variable "gcs_bucket_name" {
  description = "Nama bucket GCS"
  type        = string
  default     = "de-zoomcamp-data-lake"
}