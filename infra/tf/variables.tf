# Copyright 2023 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Project Variables

variable "prefix" {
  type        = string
  default     = null
  description = "Short uniue name for environment"
}

# GCP Project ID
variable "project_id" {
  type        = string
  description = "GCP Project Name"
}

# GCP Project Number
variable "project_number" {
  type        = string
  description = "GCP Project Number"
}

# GCP Region
variable "region" {
  type        = string
  default     = "default"
  description = "GCP Project Region"
}

# VPC Variables
variable "vpc_name" {
  type        = string
  default     = "default"
  description = "VPC Name"
}

# GKE Cluster Name
variable "gke_cluster_name" {
  type        = string
  default     = "default"
  description = "GKE Cluster Name"
}

variable "locations" {
  description = "Optional locations for GCS, BigQuery, and logging buckets created here."
  type = object({
    bq      = string
    gcs     = string
    logging = string
    pubsub  = list(string)
  })
  default = {
    bq      = "US"
    gcs     = "US"
    logging = "global"
    pubsub  = []
    region  = "us-central1"
  }
  nullable = false
}
