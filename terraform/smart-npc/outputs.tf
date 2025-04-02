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

output "INSTRUCTION" {
  value = "Please copy below outputs and save as ../data-ingestion/config-secret.toml"
}
output "database_private_ip_address" {
  value = google_sql_database_instance.postgresql.private_ip_address
}

output "database_public_ip_address" {
  value = google_sql_database_instance.postgresql.public_ip_address
}

output "postgres_instance_connection_name" {
  description = "Cloud SQL PostgreSQL connection instance name"
  value       = "${var.google_project_id}:${var.google_default_region}:${google_sql_database_instance.postgresql.name}"
}

output "database_user_name" {
  description = "Database user name"
  value       = google_sql_user.llmuser.name
}

output "database_password_key" {
  description = "Database password key"
  value       = "pgvector-password"
}

output "image_upload_gcs_bucket" {
  value = module.gcs.names_list[0]
}

output "google-project-id" {
  value = var.google_project_id
}

output "google-default-region" {
  value = var.google_default_region
}

output "cache-server-host" {
  value = google_redis_instance.cache.host
}

output "cache-server-port" {
  value = google_redis_instance.cache.port
}

output "smart-npc-https-name" {
  value = google_compute_global_address.https_static_ip_address.name
}

output "smart-npc-https-ip" {
  value = google_compute_global_address.https_static_ip_address.address
}

output "smart-npc-ws-url" {
  value = "ws://${google_compute_global_address.https_static_ip_address.name}/game/streaming"
}
