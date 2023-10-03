# Quickstart for Vertex AI Model Serving for Tensorflow

This quickstart provides a self-contained set of instructions for serving a ML model (trained as part of the [vertex_ml_training](../vertex_ml_training) quickstart). This serving framework can also be used if you already have your own trained model using Tensorflow.

---

### Prerequisites

Prior to launching the quickstart, ensure that you have successfully ran the [setup.sh](../../setup.sh) (`. setup.sh`) within the root directory of this project. This setup file will set your environment variables (which can be modified) and it will also check that your enviornment has the required services such as Terraform, the Google Cloud SDK, and any other dependencies required for this deployment.

After running the `setup.sh`, verify that a .env file has been created within your project root directory and that the `PROJECT_ROOT` env variable is set to the base path for this repo.

If all of that looks good, then you can move on to the next step.

### Step 1 - Deploy the GCP infrastructure

Before you can deploy the services within this quickstart, you will need to provision the GCP resources such as your Kubernetes cluster, services accounts, artifact registry, databases, etc. To provision your GCP resource, follow the [README](../../infra/README.md) located within the [infra](../../infra/) directory.

### Step 2 - Build the services

Run the following script that triggers the Google Cloud Build process that will build the service container and place it within Google Artifact Registry. 
<br>NOTE: The `PROJECT_ROOT` env variable should already be set, but if it is not, then make sure that you set the PROJECT_ROOT env variable to the base path for this repo.

```sh
$PROJECT_ROOT/src/ml_serving/cloudbuild_trigger.sh
```

### Step 3 - Deploy the services

Now that the service has been built and saved to Artifact Registry, we can deploy the service to Google Kubernetes Engine (GKE). To deploy the service, run this command:

```sh
$PROJECT_ROOT/quickstarts/vertex_ml_serving/deploy_to_gke.sh kubernetes.yaml
```

### Step 4 - Confirm that the model has been deployed to GKE

```sh
# Get the IP address for the exposed endpoint
kubectl get svc ml-serving-service -n game-event-ns
```

You should see that the ml-serving-serving is running with type equal to ClusterIP. With the service running, now the [event_ingest](../event_ingest) service or any other pods within the cluster can make calls to the ML endpoint in order to get predictions based on the deployed model.
