# Starting Infrastructure

This document goes over some assumed prerequisites on starting the Unified Data Framework, as well as the steps to setup the initial infrastructure.

## Pre-requisites

The Unified Data Framework assumes assumes default VPC settings and firewall rules. In the case that that those are not in place, you can view the following commands below to configure the starting point.

**VPC**

```sh
gcloud compute networks create default \
    --subnet-mode=auto \
    --bgp-routing-mode=regional \
    --mtu=1460
```

**Firewall rules**

```sh
gcloud compute firewall-rules create default-allow-internal \
  --network default \
  --allow tcp:0-65535,udp:0-65535,icmp \
  --source-ranges 10.128.0.0/9

gcloud compute firewall-rules create default-allow-ssh \
  --network default \
  --allow tcp:22 \
  --source-ranges 0.0.0.0/0

gcloud compute firewall-rules create default-allow-icmp \
  --network default \
  --allow icmp \
  --source-ranges 0.0.0.0/0
```

## [KCC] Getting started- WIP

**Pre-requisites**

In order to get started with deployment of KCC you will need to have a cluster configured with Config-Connector and connected to that cluster with your `.kubeconfig`

* [Install with GKE Add-On](https://cloud.google.com/config-connector/docs/how-to/install-upgrade-uninstall)
* [Install with other Kubernetes Distributions](https://cloud.google.com/config-connector/docs/how-to/install-other-kubernetes)
* [Other installation options](https://cloud.google.com/config-connector/docs/how-to/advanced-install)

After setup, be sure to take note of the Google Cloud service account name that will be used on behalf of our `kcc` cluster bind to workload identity to provision our infrastructure.

```sh
export GSA=YOU_SERVICE_ACCOUNT_NAME
```

This setup leverages [`kpt`](https://kpt.dev) and [`skaffold`](https://skaffold.dev/) to orchestrate our infrastructure utilizing the kubernetes resource model (KRM). With this we can extend the bare bones to operate on top of other tools for a more automated CI/CD and GitOps approch, such as Config-Sync, ArgoCD, and Cloud Deploy. 

To initiate the environment with KCC and populate with our variables run:

```sh
# GSA env variable comes from above. 

make kcc-env GSA=$GSA
```

Next we will run our skaffold pipeline to hydrate our manifest and deploy our infrastructure.

We start with configuring the config connector to run in [`cluster`](https://cloud.google.com/config-connector/docs/how-to/advanced-install#addon-configuring) mode.

```sh
skaffold run -p bootstrap-cc
```

And finally deploy UDP infrastructure

```sh
skaffold run -p bootstrap-udp
```

To tear down infra structure navigate to the udp directory.

```sh
cd k8s/udp
```

Destroy the resoureces.

```sh
kpt live destroy
```

## [Terraform] Getting started

Make sure your are running the following commands in this directory.

If you have not already done so as part of the setup.sh, then be sure to authenticate with your correct Google Cloud Project ID.

```sh
make authenticate
```

To initialize the infrastructure for UDP we will first define our environment
variables. This will make a copy of the `terraform.tfvars.sample` and create a
new file `terraform.tfvars` with the specific configurations for your
authenticated environment.

```sh
make tf-env
```

You may find that you also need to enable some project level policies.

```sh
make policy-apply
```

Finally you can run through terraform commands to provision the infrastructure.

```sh
cd tf

terraform init

terraform plan

terraform apply
```
