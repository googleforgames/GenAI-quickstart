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

# resource "google_compute_network" "solution-vpc" {
#   project                 = var.google_project_id
#   name                    = "solution-vpc"
#   auto_create_subnetworks = true
# }

resource "google_compute_router" "solution-vpc-router" {
  name    = "${var.vpc_name}-router"
  network = var.vpc_id

  bgp {
    asn = 64514
  }
}

resource "google_compute_router_nat" "nat" {
  name                               = "${var.vpc_name}-nat"
  router                             = google_compute_router.solution-vpc-router.name
  region                             = google_compute_router.solution-vpc-router.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"

  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}

resource "google_compute_firewall" "default-allows-internal" {
  name    = "allow-${var.vpc_name}-internal"
  network = var.vpc_name
  allow {
    protocol = "tcp"
  }
  allow {
    protocol = "udp"
  }
  allow {
    protocol = "icmp"
  }
  source_ranges = ["10.128.0.0/9"]
}

resource "google_compute_firewall" "allow-healthcheck" {
  name    = "allows-${var.vpc_name}-healthcheck"
  network = var.vpc_name
  allow {
    protocol = "tcp"
  }

  source_ranges = ["35.191.0.0/16", "130.211.0.0/22"]
}

resource "google_compute_global_address" "private_ip_alloc" {
  name          = "private-ip-alloc"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = var.vpc_id
}

# Create a private connection
resource "google_service_networking_connection" "servicenetworking" {
  network                 = var.vpc_id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_alloc.name]
}

resource "google_compute_network_peering_routes_config" "peering_routes" {
  peering = google_service_networking_connection.servicenetworking.peering
  network = var.vpc_name

  import_custom_routes = true
  export_custom_routes = true
}

resource "google_vpc_access_connector" "connector" {
  name          = "vpcconnector"
  ip_cidr_range = "10.8.200.0/28"
  network       = var.vpc_id
  region        = var.google_default_region
  machine_type  = "e2-micro"
  min_instances = 2
  max_instances = 3
}

# --- for HTTPS LB
resource "google_compute_global_address" "https_static_ip_address" {
  name         = "smart-npc-https-ip"
}

resource "google_dns_managed_zone" "smart-npc-zone" {
  name        = "smart-npc-zone"
  dns_name    = "gdc-demo.com."
  description = "Gemini powered NPC Demo Zone"
}

resource "google_dns_record_set" "smart-npc-https-api" {
  name = "demo.${google_dns_managed_zone.smart-npc-zone.dns_name}"
  type = "A"
  ttl  = 300

  managed_zone = google_dns_managed_zone.smart-npc-zone.name

  rrdatas = [google_compute_global_address.https_static_ip_address.address]
}
