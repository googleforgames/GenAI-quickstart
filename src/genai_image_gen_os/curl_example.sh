# Copyright 2023 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This is a sample CMD that makes a call to a Stable Diffusion 
# model, found within the Vertex GenAI Model Garden. A notebook
# can be used to train and deploy a model to a Vertex Endpoint
# and made available via Online Serving.

# USER TODO: Add values for those parameters based on your environment.
export GCP_PROJECT_ID="${GCP_PROJECT_ID}"
export VERTEX_ENDPOINT_ID="${VERTEX_ENDPOINT_ID}"

curl -X POST \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
-d '{"instances": [{ "prompt":"red car"}]}' \
https://us-central1-aiplatform.googleapis.com/v1/projects/${GCP_PROJECT_ID}/locations/us-central1/endpoints/${VERTEX_ENDPOINT_ID}:predict
