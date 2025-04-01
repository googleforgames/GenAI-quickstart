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

resource "google_project_service" "google-cloud-apis" {
  project = var.google_project_id
  for_each = toset([
    "aiplatform.googleapis.com",
    "appengine.googleapis.com",
    "artifactregistry.googleapis.com",
    "bigquery.googleapis.com",
    "bigqueryconnection.googleapis.com",
    "cloudbuild.googleapis.com",
    "cloudfunctions.googleapis.com",
    # For Eventarc GCS Trigger
    "cloudkms.googleapis.com",
    "dialogflow.googleapis.com",
    "eventarc.googleapis.com",
    "language.googleapis.com",
    "logging.googleapis.com",
    "networkconnectivity.googleapis.com",
    "pubsub.googleapis.com",
    "run.googleapis.com",
    "servicenetworking.googleapis.com",
    "secretmanager.googleapis.com",
    "sourcerepo.googleapis.com",
    "storage.googleapis.com",
    "sqladmin.googleapis.com",
    "vpcaccess.googleapis.com"
  ])
  disable_dependent_services = false
  disable_on_destroy         = false
  service                    = each.key
}

data "google_project" "project" {}
