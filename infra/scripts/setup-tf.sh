#!/bin/bash

TF_DIR=$1/tf
K8s_DIR=$1/k8s

cp $TF_DIR/terraform.tfvars.sample $TF_DIR/terraform.tfvars

sed -i "s/YOUR_GCP_PROJECT_ID/$GCP_PROJECT_ID/g" $TF_DIR/terraform.tfvars
sed -i "s/YOUR_GCP_PROJECT_NUMBER/$GCP_PROJECT_NUMBER/g" $TF_DIR/terraform.tfvars
sed -i "s/YOUR_VPC_NAME/$VPC_NAME/g" $TF_DIR/terraform.tfvars
sed -i "s/YOUR_GCP_REGION/$GCP_REGION/g" $TF_DIR/terraform.tfvars
sed -i "s/YOUR_GKE_CLUSTER_NAME/$GKE_CLUSTER_NAME/g" $TF_DIR/terraform.tfvars
