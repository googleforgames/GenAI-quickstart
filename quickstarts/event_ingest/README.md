# Quickstart for Game Telemetry

This quickstart provides a self-contained set of instructions for building and deploying the Game Telemetry services. Within this repo, we have a container service called "event_ingest", which we are using to ingest and route game telemetry to ML models, databases, etc. We're proving this event ingest service as a reference and a potential starting point, so feel free to modify it to suit your specific game telemetry needs.  

---

### Prerequisites

Prior to launching the quickstart, ensure that you have successfully ran the [setup.sh](../../setup.sh) (`. setup.sh`) within the root directory of this project. This setup file will set your environment variables (which can be modified) and it will also check that your enviornment has the required services such as Terraform, the Google Cloud SDK, and any other dependencies required for this deployment.

After running the `setup.sh`, verify that a .env file has been created within your project root directory and that the `PROJECT_ROOT` env variable is set to the base path for this repo.

If all of that looks good, then you can move on to the next step.

### Step 1 - Deploy the GCP infrastructure

Before you can deploy the services within this quickstart, you will need to provision the GCP resources such as your Kubernetes cluster, services accounts, artifact registry, databases, etc. To provision your GCP resource, follow the [README](../../infra/README.md) located within the [infra](../../infra/) directory.

### Step 2 - Build the services

Run the following script to trigger the Google Cloud Build process that will build the container and store it within Google Artifact Registry. 
<br>NOTE: The `PROJECT_ROOT` env variable should already be set, but if it is not, then make sure that you set the PROJECT_ROOT env variable to the base path of this repo.

```sh
$PROJECT_ROOT/src/event_ingest/cloudbuild_trigger.sh
```

### Step 3 - Deploy the services

Now that the service has been built and saved to Artifact Registry, we can deploy the service to Google Kubernetes Engine (GKE). To deploy the service, run this command:

```sh
# If deploying as a stand-alone service without an ML model, then run:
$PROJECT_ROOT/quickstarts/event_ingest/deploy_to_gke.sh kubernetes_without_ml.yaml

# If deploying as a service that sends game events to a pre-built ML endpoint, then run:
$PROJECT_ROOT/quickstarts/event_ingest/deploy_to_gke.sh kubernetes_with_ml.yaml
```

### Step 4 - Test the services

In order to test the service, we've provided a simple python script within this quickstart directory. The script will send a test payload to the endpoint and a response will be provided so that you can valid if the service is up and running.

```sh
# Get the IP address for the exposed endpoint
SERVICE_ENDPOINT=$(kubectl get svc event-ingest-service -n game-event-ns -o=jsonpath='{.status.loadBalancer.ingress[0].ip}')

# Send the test data to the endpoint
python3 test_tcp.py --host $SERVICE_ENDPOINT --port 80
```
