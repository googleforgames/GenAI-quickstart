#!/bin/bash
export PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# Check if gcloud SDK is installed
if ! command -v gcloud &>/dev/null; then
  echo "Please install the gcloud SDK."
  echo "https://cloud.google.com/sdk/docs/install-sdk"
  exit 1
fi

# Check if kpt is installed
if ! command -v kpt &>/dev/null; then
  echo "Please install KPT."
  echo "https://kpt.dev/installation/kpt-cli"
  exit 1
fi

# Check if Skaffold is installed
if ! command -v skaffold &>/dev/null; then
  echo "Please install skaffold."
  echo "https://skaffold.dev/docs/install/"
  exit 1
fi

# Check if user is authenticated
if ! gcloud auth list &>/dev/null; then
  echo "Please authenticate with the gcloud SDK."
  gcloud auth application-default login
fi

# Get GCP Project ID and Project Number from gcloud
export GCP_PROJECT_ID=$(gcloud config list --format 'value(core.project)' 2>/dev/null)
export GCP_PROJECT_NUMBER=$(gcloud projects describe "$GCP_PROJECT_ID" --format="value(projectNumber)" 2>/dev/null)

# Copy .env.example into a file called .env
cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"

# Update GCP PROJECT ID AND GCP PROJECT NUMBER variables
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
