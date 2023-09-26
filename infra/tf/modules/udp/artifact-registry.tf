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

resource "google_artifact_registry_repository" "udp-repo" {
  project       = var.project_id
  location      = var.pipeline.artifact_registry.location
  repository_id = var.pipeline.artifact_registry.repository_name
  description   = var.pipeline.artifact_registry.description
  format        = var.pipeline.artifact_registry.format
}
