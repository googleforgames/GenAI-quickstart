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

module "vpc" {
  source  = "terraform-google-modules/network/google"
  version = "8.0.0"

  project_id   = var.project_id
  network_name = "vpc-genai-quickstart"
  routing_mode = "GLOBAL"

  subnets = [
    {
      subnet_name           = "sn-usw1"
      subnet_ip             = "10.11.16.0/20"
      subnet_region         = "us-west1"
      subnet_private_access = "true"
      subnet_flow_logs      = "false"
      description           = "Subnet for US West1"
    }
  ]

  secondary_ranges = {
    "sn-usw1" = [
      {
        range_name    = "sn-usw1-pods1"
        ip_cidr_range = "10.11.0.0/20"
      },
      {
        range_name    = "sn-usw1-svcs1"
        ip_cidr_range = "10.111.0.0/25"
      },
    ]
  }

  ingress_rules = [
    {
      name          = "fw-game-server"
      description   = "Allow game server traffic"
      priority      = 1000
      source_ranges = ["0.0.0.0/0"],
      target_tags   = ["game-server"]
      allow = [
        {
          protocol = "udp"
          ports    = ["7000-8000"]
        }
      ]
    }
  ]
}
