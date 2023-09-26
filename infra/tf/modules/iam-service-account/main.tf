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
  prefix                = var.prefix == null ? "" : "sa-${var.prefix}-"
  resource_email_static = "${local.prefix}${var.name}@${var.project_id}.iam.gserviceaccount.com"
  resource_iam_email = (
    local.service_account != null
    ? "serviceAccount:${local.service_account.email}"
    : local.resource_iam_email_static
  )
  resource_iam_email_static = "serviceAccount:${local.resource_email_static}"
  service_account_id_static = "projects/${var.project_id}/serviceAccounts/${local.resource_email_static}"
  service_account = (
    var.service_account_create
    ? try(google_service_account.service_account.0, null)
    : try(data.google_service_account.service_account.0, null)
  )
}

data "google_service_account" "service_account" {
  count      = var.service_account_create ? 0 : 1
  project    = var.project_id
  account_id = "${local.prefix}${var.name}"
}

resource "google_service_account" "service_account" {
  count        = var.service_account_create ? 1 : 0
  project      = var.project_id
  account_id   = "${local.prefix}${var.name}"
  display_name = var.display_name
  description  = var.description
}
