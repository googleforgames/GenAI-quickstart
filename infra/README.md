# Starting Infrastructure

This README provides the steps required to setup the initial infrastructure.

## Pre-requisites

This project assumes assumes default VPC settings and firewall rules. In the case that that those are not in place, you can view the following commands below to configure the starting point.

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

## [Terraform] Getting started

Make sure your are running the following commands in this directory.

If you have not already done so as part of the setup.sh, then be sure to authenticate with your correct Google Cloud Project ID.

```sh
cd $PROJECT_ROOT/infra
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
cd $PROJECT_ROOT/infra/tf

terraform init

terraform plan

terraform apply
```
