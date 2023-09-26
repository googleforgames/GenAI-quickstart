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
  description = "Short unique name for environment"
}

variable "project_id" {
  type        = string
  description = "GCP Project Name"
}

variable "project_number" {
  type        = string
  description = "GCP Project Number"
}

variable "services" {
  type        = list(any)
  description = "GCP Service APIs to enable for this project"
  default     = []
}

variable "iam" {
  description = "Project-level IAM settings."
  type        = map(list(string))
  default     = {}
}

# VPC Variables
variable "vpc_name" {
  type        = string
  description = "VPC Name"
}

# GKE Variables
variable "gke_config" {
  type        = map(any)
  default     = {}
  description = "GKE Cluster configs"
}

# Spanner Variables
variable "spanner_config" {
  type        = map(any)
  description = "Spanner configs"
}

# BigQuery Variables
variable "bigquery_config" {
  type = object({
    dataset     = string,
    location    = string,
    description = string,
    tables      = map(any),
  })
  description = "BigQuery Dataset for Unified Data"
}

# PubSub Variables
variable "game_telemetry_topic" {
  type        = string
  description = "PubSub Topic for Game Telemetry"
}

# Pipeline Variables
variable "pipeline" {
  type = object({
    artifact_registry = object({
      location        = string
      repository_name = string
      description     = string
      format          = string
    })
  })
  description = "Configuraion for UDP automation pipeline"
}

