# GenAI Quickstart Infrastructure

This creates the infrastructure for the GenAI quickstart guide.

## How to run

`terraform init`

`terraform plan`

`terraform apply`

`terraform destroy`

## Architecture and Design

![Alt GKE Architecture](../docs/img/genai-gke-arch.svg)

## IAM bindings reference

Legend: <code>+</code> additive, <code>•</code> conditional.

### Organization <i>[org_id]</i>

| members | roles |
|---|---|

### Project <i>[project_id]</i>

| members | roles |
|---|---|
|<b>user</b><br><small><i>User</i></small>|[roles/owner](https://cloud.google.com/iam/docs/understanding-roles#owner) <code>+</code> |
|<b>sa-gke-cluster</b><br><small><i>Service account</i></small>|[roles/artifactregistry.reader](https://cloud.google.com/iam/docs/understanding-roles#artifactregistry.reader) <code>+</code> · [roles/container.developer](https://cloud.google.com/iam/docs/understanding-roles#container.developer) <code>+</code> · [roles/container.nodeServiceAgent](https://cloud.google.com/iam/docs/understanding-roles#container.nodeServiceAgent) <code>+</code> · [roles/logging.logWriter](https://cloud.google.com/iam/docs/understanding-roles#logging.logWriter) <code>+</code> · [roles/monitoring.metricWriter](https://cloud.google.com/iam/docs/understanding-roles#monitoring.metricWriter) <code>+</code> · [roles/monitoring.viewer](https://cloud.google.com/iam/docs/understanding-roles#monitoring.viewer) <code>+</code> · [roles/stackdriver.resourceMetadata.writer](https://cloud.google.com/iam/docs/understanding-roles#stackdriver.resourceMetadata.writer) <code>+</code> |
|<b>sa-gke-aiplatform</b><br><small><i>Service account</i></small>|[roles/aiplatform.user](https://cloud.google.com/iam/docs/understanding-roles#aiplatform.user) <code>+</code> · [roles/storage.user](https://cloud.google.com/iam/docs/understanding-roles#storage.user) <code>+</code>|
|<b>sa-gke-telemetry</b><br><small><i>Service account</i></small>|[roles/cloudtrace.agent](https://cloud.google.com/iam/docs/understanding-roles#cloudtrace.agent) <code>+</code>|


## Files

| name | description | modules | resources |
|---|---|---|---|
| [bootstrap.tf](./bootstrap.tf) | Bootstrapping prerequisites for project. |  |  |
| [cicd.tf](./gke.tf) | Recources created to CI/CD pipeline. |  | `google_artifact_registry_repository` |
| [gke.tf](./gke.tf) | GKE cluster with game server and GPU nodepools for GenAI. | [`gke`](https://registry.terraform.io/modules/terraform-google-modules/kubernetes-engine/google/latest/submodules/beta-private-cluster) |  |
| [iam.tf](./gke.tf) | IAM resources for project needed by Cloud resources. | [`member_roles_gke`, `member_roles_aiplatform`, `member_roles_telemetry`, `member_roles_cloudbuild`](https://registry.terraform.io/modules/terraform-google-modules/iam/google/latest/submodules/member_iam) | `google_service_account.sa_gke_cluster`, `google_service_account.sa_gke_aiplatform`, `google_service_account.sa_gke_telemetry` · `google_service_account_iam_binding.sa_gke_cluster_wi_binding`, `google_service_account_iam_binding.sa_gke_aiplatform_wi_binding`, `google_service_account_iam_binding.sa_gke_telemetry_wi_binding` |
| [net.tf](./net.tf) | VPC network and firewall rules. | [`vpc`](https://registry.terraform.io/modules/terraform-google-modules/network/google/latest) |  |


## Variables

| name | description | type | required | default |
|---|---|:---:|:---:|:---:|
| project_id | Unique project ID to host project resources. | `string` | ✓ | "" |

## Outputs

| name | description | sensitive | consumers |
|---|---|:---:|---|