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

resource "null_resource" "workstation_public_ip" {
  provisioner "local-exec" {
    command = <<EOF
      curl ifconfig.me
EOF
  }
}
resource "google_sql_database_instance" "postgresql" {
  name             = "pgvector-db"
  database_version = "POSTGRES_14"
  region           = var.google_default_region

  settings {
    availability_type = "REGIONAL"
    tier              = "db-custom-2-8192"
    disk_size         = "10"
    disk_type         = "PD_SSD"
    disk_autoresize   = "true"
    ip_configuration {
      ipv4_enabled    = "true"
      private_network = var.vpc_id

      # dynamic "authorized_networks" {
      #   content {
      #     name  = "allow-workstation"
      #     value = null_resource.workstation_public_ip.stdout
      #   }
      # }
      authorized_networks {
        name  = "Cloud Top 5"
        value = "34.29.82.0/24"
      }
      authorized_networks {
        name  = "Cloud top 5 - 2"
        value = "104.198.173.0/24"
      }
    }

    database_flags {
      name  = "cloudsql.iam_authentication"
      value = "on"
    }
  }

  depends_on = [google_service_networking_connection.servicenetworking]
}


resource "google_sql_user" "llmuser" {
  name     = "llmuser"
  instance = google_sql_database_instance.postgresql.name
  password = random_password.password.result
}

resource "google_sql_user" "iam_service_account_user" {
  # Note: for Postgres only, GCP requires omitting the ".gserviceaccount.com" suffix
  # from the service account email due to length limits on database usernames.
  name     = trimsuffix(google_service_account.app-service-account.email, ".gserviceaccount.com")
  instance = google_sql_database_instance.postgresql.name
  type     = "CLOUD_IAM_SERVICE_ACCOUNT"
}
