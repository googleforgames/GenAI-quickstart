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

# google_client_config and kubernetes provider must be explicitly specified like the following.
data "google_client_config" "default" {}

provider "kubernetes" {
  host                   = "https://${module.gke.endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(module.gke.ca_certificate)
}

module "gke" {
  source                     = "terraform-google-modules/kubernetes-engine/google//modules/beta-autopilot-public-cluster"
  version                    = "29.0.0"

  project_id                 = var.project_id
  name                       = "genai-quickstart"
  region                     = "us-central1"
  network                    = module.vpc.network_name
  subnetwork                 = "sn-usc1"
  ip_range_pods              = "sn-usc1-pods1"
  ip_range_services          = "sn-usc1-svcs1"
  horizontal_pod_autoscaling = true
  release_channel            = "RAPID" # RAPID was chosen for L4 support.
  kubernetes_version         = "1.28"  # We need the tip of 1.28 or 1.29 (not just default)
  service_account            = google_service_account.sa_gke_cluster.email

  # Need to allow 48 hour window in rolling 32 days For `maintenance_start_time`
  # & `end_time` only the specified time of the day is used, the specified date
  # is ignored (https://cloud.google.com/composer/docs/specify-maintenance-windows#terraform)
  maintenance_recurrence = "FREQ=WEEKLY;BYDAY=SU"
  maintenance_start_time = "2023-01-02T07:00:00Z"
  maintenance_end_time   = "2023-01-02T19:00:00Z"

  depends_on = [
    google_service_account.sa_gke_cluster,
    module.vpc
  ]
}

