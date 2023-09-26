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

module "udp" {
  source = "./modules/udp"
  services = [
    "cloudbuild.googleapis.com",
    "compute.googleapis.com",
    "container.googleapis.com",
    "artifactregistry.googleapis.com",
    "spanner.googleapis.com",
    "servicecontrol.googleapis.com",
    "run.googleapis.com",
    "containerregistry.googleapis.com",
    "pubsub.googleapis.com",
  ]

  project_id = var.project_id
  project_number = var.project_number

  # VPC
  vpc_name = "default"

  # IAM
  iam = {
    "roles/aiplatform.serviceAgent" = [
      module.iam_sa_cloudbuild.iam_email,
      "serviceAccount:${var.project_number}@cloudbuild.gserviceaccount.com"
    ]
    "roles/cloudbuild.builds.builder" = [
      module.iam_sa_cloudbuild.iam_email
    ]
    "roles/clouddeploy.operator" = [
      module.iam_sa_cloudbuild.iam_email
    ]
    "roles/container.admin" = [
      module.iam_sa_cloudbuild.iam_email
    ]
    "roles/iam.serviceAccountUser" = [
      module.iam_sa_cloudbuild.iam_email,
      "serviceAccount:${var.project_number}@cloudbuild.gserviceaccount.com"
    ]
    "roles/serviceusage.serviceUsageAdmin" = [
      module.iam_sa_cloudbuild.iam_email
    ]
    "roles/storage.admin" = [
      module.iam_sa_cloudbuild.iam_email
    ]
    "roles/spanner.databaseUser" = [
      module.iam_sa_spanner.iam_email
    ]
    "roles/storage.objectViewer" = [
      "serviceAccount:${var.project_number}@cloudbuild.gserviceaccount.com"
    ]
    "roles/artifactregistry.writer" = [
      "serviceAccount:${var.project_number}@cloudbuild.gserviceaccount.com"
    ]
  }

  # GKE Cluster Configs
  gke_config = {
    "unified-data-us-central1" = {
      region       = "us-central1",
      machine_type = "e2-standard-4",
    }
  }

  # Spanner Config
  spanner_config = {
    instance_name    = "unified-data-instance",
    db_name          = "unified-data",
    location         = "nam9",
    processing_units = 100,
  }

  # BigQuery
  bigquery_config = {
    dataset     = "unified_data",
    location    = "${var.locations.bq}",
    description = "Unified Data",
    tables = {
      "game_telemetry" = {
        name = "game_telemetry",
      }
    }
  }

  # PubSub
  game_telemetry_topic = "game_telemetry_topic"

  # Pipeline
  pipeline = {
    artifact_registry = {
      location        = "us-central1",
      repository_name = "udp-repo",
      description     = "Docker repo for UDP Assets",
      format          = "DOCKER",
    }
  }
}

module "iam_sa_cloudbuild" {
  source      = "./modules/iam-service-account"
  project_id  = var.project_id
  name        = "cloudbuild-cicd"
  description = "TF - Cloud Build SA"
}

module "iam_sa_spanner" {
  source      = "./modules/iam-service-account"
  project_id  = var.project_id
  name        = "spanner-sa"
  description = "TF - Spanner SA"
}

module "tf-state-gcs" {
  source     = "./modules/gcs"
  project_id = var.project_id
  name       = "${var.project_id}-tf-state"
  location   = var.locations.gcs
  versioning = true
}

module "bkt-ml-models" {
  source        = "./modules/gcs"
  project_id    = var.project_id
  name          = "${var.project_id}-models"
  location      = var.locations.gcs
  versioning    = true
  force_destroy = true
}
