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

locals {
  prefix = var.prefix == null ? "" : "bkt-${var.prefix}-"
}

resource "google_storage_bucket" "bucket" {
  name                        = "${local.prefix}${lower(var.name)}"
  project                     = var.project_id
  location                    = var.location
  storage_class               = var.storage_class
  force_destroy               = var.force_destroy
  uniform_bucket_level_access = var.uniform_bucket_level_access
  labels                      = var.labels
  versioning {
    enabled = var.versioning
  }
}

resource "google_storage_bucket_iam_binding" "bindings" {
  for_each = var.iam
  bucket   = google_storage_bucket.bucket.name
  role     = each.key
  members  = each.value
}
