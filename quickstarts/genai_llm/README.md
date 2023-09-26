# Quickstart for Google LLMs

This quickstart provides a self-contained set of instructions for building and deploying a service that integrates with Google Vertex LLMs (Large Language Models).

This service can be configured to work with the following LLMs: 

- [Text Model](https://cloud.google.com/vertex-ai/docs/generative-ai/text/text-overview): Fine-tuned to follow natural language instructions for Q&A, classification, summarization, sentiment, and more.
- [Chat Model](https://cloud.google.com/vertex-ai/docs/generative-ai/chat/chat-prompts): Fine-tuned for multi-turn conversation use cases.
- [Code Model](https://cloud.google.com/vertex-ai/docs/generative-ai/code/code-generation-prompts): Fine-tuned to generate code based on a natural language description of the desired code.


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
$PROJECT_ROOT/src/genai_llm/cloudbuild_trigger.sh
```

### Step 3 - Deploy the services

Now that the service has been built and saved to Artifact Registry, we can deploy the service to Google Kubernetes Engine (GKE). To deploy the service, run this command:

```sh
# Ensure that the ENV variables are set in your .env or set them prior to deploying to GKE.
export GCP_PROJECT_ID="your_gcp_project_id"
export MODEL_TYPE="text-bison"  # This can be "text-bison", "chat-bison", "code-bison", or "codechat-bison"

$PROJECT_ROOT/quickstarts/genai_llm/deploy_to_gke.sh kubernetes.yaml
```

### Step 4 - Test the GenAI Endpoint

We've provided a simple REST command that sends test data to the deployed GenAI LLM service. 

```sh
# Get the IP address for the exposed endpoint
SERVICE_ENDPOINT=$(kubectl get svc genai-llm-vertex-service -n ai-ns -o=jsonpath='{.status.loadBalancer.ingress[0].ip}')

# Send the test data to the endpoint (GET request)
curl "http://$SERVICE_ENDPOINT/llm?prompt=When%20was%20google%20founded?"

# Send the test data to the endpoint (POST request)
curl -X POST -H "Content-Type: application/json" -d '{"prompt":"When was google founded?"}' "http://$SERVICE_ENDPOINT/llm"
```
