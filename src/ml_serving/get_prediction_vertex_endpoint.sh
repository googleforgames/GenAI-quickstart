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

# NOTE: This script is provided as an example and used for adhoc testing. It can be removed or edited at anytime.

export GCP_PROJECT_ID=$GCP_PROJECT_ID
export VERTEX_ENDPOINT_ID="123456789123456789"   # Set your own Vertex Endpoint ID

curl \
-X POST \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
https://us-central1-aiplatform.googleapis.com/v1/projects/${GCP_PROJECT_ID}/locations/us-central1/endpoints/${VERTEX_ENDPOINT_ID}:predict \
-d '{"instances": [[1.4838871833555929, -1.8659883497083019, -2.234620276849616, 1.0187816540094903, 2.530890710602246, 0.6046416850441676, 0.4651483719733302, 2.4952254087173721, 1.7746763768735953]]}'

# Column Names
# x, y, z, score, bonus, offensePct, defensePct, minutesPlayed, timeInStore
