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

resource "google_redis_instance" "cache" {
  name           = "npc-cache"
  tier           = "BASIC"
  memory_size_gb = 1

  location_id = var.google_default_zone
  #   alternative_location_id = "us-central1-f"

  authorized_network = var.vpc_id

  redis_version = "REDIS_4_0"
  display_name  = "NPC Cache"

  lifecycle {
    prevent_destroy = true
  }
}
