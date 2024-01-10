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

provider "kubernetes" {
  host                   = "https://${module.gke.endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(module.gke.ca_certificate)
}

data "google_client_config" "default" {}

module "gke" {
  source  = "terraform-google-modules/kubernetes-engine/google//modules/beta-public-cluster"
  version = "29.0.0"

  project_id                 = var.project_id
  name                       = "genai-quickstart"
  regional                   = false
  region                     = "us-west1"
  zones                      = ["us-west1-b"]
  network                    = module.vpc.network_name
  subnetwork                 = "sn-usw1"
  ip_range_pods              = "sn-usw1-pods1"
  ip_range_services          = "sn-usw1-svcs1"
  remove_default_node_pool   = true
  http_load_balancing        = true
  default_max_pods_per_node  = 32
  horizontal_pod_autoscaling = true
  filestore_csi_driver       = false
  release_channel            = "REGULAR"
  identity_namespace         = "enabled"
  create_service_account     = false
  service_account            = google_service_account.sa_gke_cluster.email
  enable_shielded_nodes      = true
  # enable_gcfs	               = true # Cluster wide image streaming
  deletion_protection        = false

  # Need to allow 48 hour window in rolling 32 days For `maintenance_start_time`
  # & `end_time` only the specified time of the day is used, the specified date
  # is ignored (https://cloud.google.com/composer/docs/specify-maintenance-windows#terraform)
  maintenance_recurrence = "FREQ=WEEKLY;BYDAY=SU"
  maintenance_start_time = "2023-01-02T07:00:00Z"
  maintenance_end_time   = "2023-01-02T19:00:00Z"

  cluster_autoscaling = {
    auto_repair         = true
    auto_upgrade        = true
    autoscaling_profile = "OPTIMIZE_UTILIZATION"
    # NAP configurations (disabled by default)
    enabled       = false
    min_cpu_cores = 0
    max_cpu_cores = 0
    min_memory_gb = 0
    max_memory_gb = 0
    gpu_resources = []
  }

  node_pools = [
    {
      # CPU based nodepool
      name                        = "nodepool-cpu"
      default-node-pool           = true
      machine_type                = "e2-standard-2"
      image_type                  = "COS_CONTAINERD"
      disk_size_gb                = 100
      disk_type                   = "pd-standard"
      autoscaling                 = true
      enable_secure_boot          = true
      enable_integrity_monitoring = true
      enable_gcfs                 = true
      initial_node_count          = 1
      min_count                   = 1
      max_count                   = 5
      location_policy             = "ANY"
    },
    {
      # GPU based nodepool
      name                        = "nodepool-gpu"
      machine_type                = "n1-standard-2"
      accelerator_type            = "nvidia-tesla-t4"
      accelerator_count           = 1
      gpu_driver_version          = "DEFAULT" #can be set to "LATEST" or "DEFAULT"
      image_type                  = "COS_CONTAINERD"
      disk_size_gb                = 100
      disk_type                   = "pd-standard"
      autoscaling                 = true
      enable_secure_boot          = true
      enable_integrity_monitoring = true
      enable_gcfs                 = true
      initial_node_count          = 0
      min_count                   = 0
      max_count                   = 2
      location_policy             = "ANY"
    }
  ]

  node_pools_oauth_scopes = {
    all = [
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
      "https://www.googleapis.com/auth/trace.append",
      "https://www.googleapis.com/auth/devstorage.read_only",
      "https://www.googleapis.com/auth/service.management.readonly",
      "https://www.googleapis.com/auth/servicecontrol",
    ]
  }

  node_pools_tags = {
    all = []

    "nodepool-cpu" = [
      "default",
      "cpu",
      "game-server",
    ]

    "nodepool-gpu" = [
      "gpu",
    ]
  }

  node_pools_taints = {
    all = []

    "nodepool-gpu" = [
      {
        key    = "nvidia.com/gpu"
        value  = true
        effect = "NO_SCHEDULE"
      },
    ]
  }

  depends_on = [
    google_service_account.sa_gke_cluster,
    module.vpc
  ]
}
