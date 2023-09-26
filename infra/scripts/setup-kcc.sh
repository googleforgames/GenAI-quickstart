#!/bin/bash
CUR_DIR=$1
K8S_DIR=$1/k8s
PKG_DIR=$1/pkg

GSA=$2

rm -rf $K8S_DIR/*

# [TODO] eventually use this when pushed to main
# kpt pkg get git@github.com:googleforgames/gaming-specialists.git/udp/infra/pkg@main $K8S_DIR

cp -r $PKG_DIR/udp $K8S_DIR
cp -r $PKG_DIR/configconnector $K8S_DIR

sed -i "s/your-project-id/$GCP_PROJECT_ID/g" $K8S_DIR/udp/setters.yaml
sed -i "s/your-gsa/$GSA/g" $K8S_DIR/udp/setters.yaml

sed -i "s/your-project-id/$GCP_PROJECT_ID/g" $K8S_DIR/configconnector/setters.yaml
sed -i "s/your-gsa/$GSA/g" $K8S_DIR/configconnector/setters.yaml

kpt fn render $K8S_DIR/udp
kpt fn render $K8S_DIR/configconnector
