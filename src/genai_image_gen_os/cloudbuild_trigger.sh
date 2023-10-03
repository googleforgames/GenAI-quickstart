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

SCRIPT_DIR=$(dirname $(realpath "$0"))

gcloud builds submit \
"$SCRIPT_DIR" \
--substitutions=_GCP_PROJECT_ID="$GCP_PROJECT_ID",\
_ARTIFACT_REPO_REGION="$ARTIFACT_REPO_REGION",\
_ARTIFACT_REPO_NAME="$ARTIFACT_REPO_NAME",\
_IMAGE_NAME="genai-image-gen-os" \
--region="$GCP_REGION" \
--config "$SCRIPT_DIR/cloudbuild.yaml"
