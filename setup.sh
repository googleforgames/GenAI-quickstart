#!/bin/bash

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

export PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# Check if the gcloud SDK is installed
if ! command -v gcloud &>/dev/null; then
  echo "Please install the gcloud SDK."
  echo "https://cloud.google.com/sdk/docs/install-sdk"
  exit 1
fi

# Check if Terraform is installed
if ! command -v terraform &>/dev/null; then
  echo "Please install Terraform."
  echo "https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/install-cli"
  exit 1
fi

# Check if user is authenticated to gcloud
if ! gcloud auth list &>/dev/null; then
  echo "Please authenticate with the gcloud SDK."
  gcloud auth application-default login
fi

# Use gcloud to get the GCP Project ID and Project Number
export GCP_PROJECT_ID=$(gcloud config list --format 'value(core.project)' 2>/dev/null)
export GCP_PROJECT_NUMBER=$(gcloud projects describe "$GCP_PROJECT_ID" --format="value(projectNumber)" 2>/dev/null)

# Copy .env.example into a file called .env if the .env does not already exist.
if [ -e "$PROJECT_ROOT/.env" ]; then
    echo ".env file already exists."
else
    cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
    echo ".env file created successfully."
fi

# Update GCP PROJECT ID AND GCP PROJECT NUMBER variables within the .env
sed -i "s/YOUR_GCP_PROJECT_ID/$GCP_PROJECT_ID/g" "$PROJECT_ROOT/.env"
sed -i "s/YOUR_GCP_PROJECT_NUMBER/$GCP_PROJECT_NUMBER/g" "$PROJECT_ROOT/.env"

# Set ENV variables
. "$PROJECT_ROOT/.env"

# Enable Google Cloud APIs required for deployments
gcloud services enable \
cloudresourcemanager.googleapis.com \
cloudbuild.googleapis.com \
compute.googleapis.com \
container.googleapis.com \
artifactregistry.googleapis.com \
spanner.googleapis.com \
servicecontrol.googleapis.com \
run.googleapis.com \
containerregistry.googleapis.com \
pubsub.googleapis.com \
aiplatform.googleapis.com

echo ""
echo "********************************************"
echo ""
echo "Setup Complete!"
echo ""
echo "Using GCP Project: ${GCP_PROJECT_ID}"
echo ""
echo "Environment variables for this deployment"
echo "can be found within the .env file"
echo ""
echo "********************************************"
echo ""
