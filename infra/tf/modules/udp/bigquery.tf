// Copyright 2023 Google LLC All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

resource "google_bigquery_dataset" "default" {
  project       = var.project_id
  dataset_id    = var.bigquery_config.dataset
  friendly_name = var.bigquery_config.dataset
  description   = "Unified Data"
  location      = var.bigquery_config.location
}

# TOOD - Add BQ tables w/ schema
resource "google_bigquery_table" "default" {
  for_each   = var.bigquery_config.tables
  project    = var.project_id
  dataset_id = google_bigquery_dataset.default.dataset_id
  table_id   = each.key
}
