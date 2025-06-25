# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

resource "google_service_account" "app-service-account" {
  account_id   = "app-service-account"
  display_name = "Application Service Account"
}

resource "google_project_iam_member" "app-service-account" {
  project = var.google_project_id
  for_each = toset([
    # Cloud SQL Client
    "roles/cloudsql.client",
    # Invoke Generative AI services
    "roles/aiplatform.user",
    # Log Writer
    "roles/logging.logWriter",
    # Able to upload and download conversation logs from GCS
    "roles/storage.objectCreator",
    "roles/storage.objectViewer",
    # Need storage.objects.delete
    "roles/storage.objectAdmin",
    # For Gen2 cloud functions invoker
    "roles/run.invoker",
    # For Secret Manager
    "roles/secretmanager.secretAccessor",
    # For deploying to Cloud Run using this service account
    "roles/iam.serviceAccountUser",
  ])
  role   = each.key
  member = "serviceAccount:${google_service_account.app-service-account.email}"
  depends_on = [
    google_project_service.google-cloud-apis,
  ]
}

# https://cloud.google.com/eventarc/docs/run/create-trigger-storage-gcloud#before-you-begin
# resource "google_project_service_identity" "storage_service_agent" {
#   provider = google-beta
#   project  = var.google_project_id
#   service  = "storage.googleapis.com"
#   depends_on = [
#     google_project_service.google-cloud-apis
#   ]
# }
