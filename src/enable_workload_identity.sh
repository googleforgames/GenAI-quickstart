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


# NOTE: This utility script can be used to configure worload identity 
# for the GKE Autopilot cluster. This provides a working example used 
# for our demo, and future updates will further integrate this into 
# our infra (tf) deployment. 


# Get GKE Cluster Credentials
gcloud container clusters get-credentials $GKE_CLUSTER_NAME --region $GCP_REGION --project $GCP_PROJECT_ID


# Create Service Account
gcloud iam service-accounts create gke-sa \
    --project=$GCP_PROJECT_ID


# Add Role(s) to Service Account
gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
    --member "serviceAccount:gke-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
    --role "roles/editor"


################################
#
#   Game Event Namespace
#
################################


# Create Namespace
kubectl create namespace game-event-ns


# Create service account in namespace
kubectl create serviceaccount gke-k8s-sa \
    --namespace game-event-ns


# Allow the Kubernetes service account to impersonate the IAM service account 
# by adding an IAM policy binding between the two service accounts.
gcloud iam service-accounts add-iam-policy-binding gke-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com \
    --role roles/iam.workloadIdentityUser \
    --member "serviceAccount:$GCP_PROJECT_ID.svc.id.goog[game-event-ns/gke-k8s-sa]"


# Annotate the Kubernetes service account with the email address of the IAM service account
kubectl annotate serviceaccount gke-k8s-sa \
    --namespace game-event-ns \
    iam.gke.io/gcp-service-account=gke-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com


################################
#
#   Gen AI Namespace
#
################################


# Create Namespace
kubectl create namespace ai-ns


# Create service account in namespace
kubectl create serviceaccount gke-k8s-sa \
    --namespace ai-ns


# Allow the Kubernetes service account to impersonate the IAM service account 
# by adding an IAM policy binding between the two service accounts.
gcloud iam service-accounts add-iam-policy-binding gke-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com \
    --role roles/iam.workloadIdentityUser \
    --member "serviceAccount:$GCP_PROJECT_ID.svc.id.goog[ai-ns/gke-k8s-sa]"


# Annotate the Kubernetes service account with the email address of the IAM service account
kubectl annotate serviceaccount gke-k8s-sa \
    --namespace ai-ns \
    iam.gke.io/gcp-service-account=gke-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com
