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

data "google_project" "project" {
  project_id = var.project_id
}

# Create a service account for GKE cluster
resource "google_service_account" "sa_gke_cluster" {
  account_id   = "sa-gke-cluster"
  display_name = "TF - GKE cluster SA"
  project      = var.project_id
}

resource "google_service_account_iam_binding" "sa_gke_cluster_wi_binding" {
  service_account_id = google_service_account.sa_gke_cluster.name
  role               = "roles/iam.workloadIdentityUser"
  members = [
    "serviceAccount:${var.project_id}.svc.id.goog[genai/k8s-sa-cluster]",
  ]
}

module "member_roles_gke_cluster" {
  source                  = "terraform-google-modules/iam/google//modules/member_iam"
  service_account_address = google_service_account.sa_gke_cluster.email
  prefix                  = "serviceAccount"
  project_id              = var.project_id
  project_roles = [
    "roles/artifactregistry.reader",
    "roles/container.developer",
    "roles/container.nodeServiceAgent",
    "roles/logging.logWriter",
    "roles/monitoring.metricWriter",
    "roles/monitoring.viewer",
    "roles/stackdriver.resourceMetadata.writer",
    "roles/cloudtrace.agent",
  ]
}

# Create a service account for GKE AI Platform access to Vertex AI
resource "google_service_account" "sa_gke_aiplatform" {
  account_id   = "sa-gke-aiplatform"
  display_name = "TF - GKE ai platform SA"
  project      = var.project_id
}

resource "google_service_account_iam_binding" "sa_gke_aiplatform_wi_binding" {
  service_account_id = google_service_account.sa_gke_aiplatform.name
  role               = "roles/iam.workloadIdentityUser"
  members = [
    "serviceAccount:${var.project_id}.svc.id.goog[genai/k8s-sa-aiplatform]",
  ]
}

module "member_roles_gke_aiplatform" {
  source                  = "terraform-google-modules/iam/google//modules/member_iam"
  service_account_address = google_service_account.sa_gke_aiplatform.email
  prefix                  = "serviceAccount"
  project_id              = var.project_id
  project_roles = [
    "roles/aiplatform.user",
    "roles/storage.objectUser",
  ]
}

# Create a service account for GKE telemetry collection
resource "google_service_account" "sa_gke_telemetry" {
  account_id   = "sa-gke-telemetry"
  display_name = "TF - GKE telemetry collection SA"
  project      = var.project_id
}

resource "google_service_account_iam_binding" "sa_gke_telemetry_wi_binding" {
  service_account_id = google_service_account.sa_gke_telemetry.name
  role               = "roles/iam.workloadIdentityUser"
  members = [
    "serviceAccount:${var.project_id}.svc.id.goog[genai/k8s-sa-telemetry]",
  ]
}

module "member_roles_gke_telemetry" {
  source                  = "terraform-google-modules/iam/google//modules/member_iam"
  service_account_address = google_service_account.sa_gke_telemetry.email
  prefix                  = "serviceAccount"
  project_id              = var.project_id
  project_roles = [
    "roles/cloudtrace.agent",
  ]
}

# Add roles to the default Cloud Build service account
module "member_roles_cloudbuild" {
  source                  = "terraform-google-modules/iam/google//modules/member_iam"
  service_account_address = "${data.google_project.project.number}@cloudbuild.gserviceaccount.com"
  prefix                  = "serviceAccount"
  project_id              = var.project_id
  project_roles = [
    "roles/artifactregistry.repoAdmin",
    "roles/cloudbuild.connectionAdmin",
    "roles/cloudbuild.builds.builder",
    "roles/container.developer",
    "roles/storage.objectAdmin",
  ]
}
