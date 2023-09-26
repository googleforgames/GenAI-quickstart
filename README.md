# Unified Data Framework for Games

This project provides an end-to-end data framework to support the personalization of live game enviroments using Google Cloud products and open source gaming solutions. The framework may be used in it's entirely, or as components. 

If you’re using this framework, please ★Star this repository to show your interest!

Projects and products utilised include:

*   [Unity](https://unity.com/) for the game client and server code.
*   A custom [Go](https://go.dev/) API service.
*   [Terraform](https://www.terraform.io/), for infrastructure as code.
*   [Cloud Build](https://cloud.google.com/build) and [Cloud Deploy](https://cloud.google.com/deploy) for Continuous Integration and Deployment.
*   [GKE Autopilot](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview) for hosting the backend microservices.
*   Globally distributed [GKE](https://cloud.google.com/kubernetes-engine) Autopilot and/or Standard clusters running [Agones](https://agones.dev/) for hosting and scaling dedicated game servers.
*   [Vertex AI](https://cloud.google.com/vertex-ai) for training, deploying, and hosting machine learning models
*   [Cloud Spanner](https://cloud.google.com/spanner) for storing the player in-game data.

# Architecture 

## Project Structure 

| Folder                             | Description                                                                                                                                                                                                                                                                                   |
|------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Infrastructure](./infr) | This contains all Terraform |
| [Quickstarts](./quickstarts)       | Individual Componants of the Framework that can be run disctinctly from each other |
| [Services](./services)             | Services |
| [Machine Learning](./ml)           | Machine Learning |
| [Simulators](./simulators)         | Utilities for simulated game traffic |

## Architecture Diagram 

This repo contains the following framework components: 

- Demos to highlight various features of our framework
- Load Testing Scripts (used for benchmarking peformance

![Architecture](images/architecture.png)


NOTE: This is a rapidly evolving repo and is being adapted for a variety of use cases. If you would like to contribute or notice any bugs, please open an issue and/or feel free to submit a PR for review.

<br>

# Running the Framework

## Setup

Run the [setup.sh](setup.sh) prior to your deployment. This setup script will check for system dependencies (such as gcloud, terraform, etc), it will set default ENV variables, and enable Google Cloud APIs required for the deployment.

```sh
# Run the setup script
source ./setup.sh
```

## Provision Cloud Infrastructure on GCP

To provision the infrastructure, follow the instructions provided at [infra/README.md](./infra/README.md). 

<br>

## Quickstarts

At this point, if you'd like to deploy modular parts of the framework, then navigate to the section that is most relevent for your use case based on the options below: 

| Quick Start Name                   | Description                                                                                                                                                                                                                                                                                   |
|------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Event Ingest](./quickstarts/event_ingest) | This service ingests game telemetry from the game server. It is responsible for accepting and routing the game event traffic. |
| [Spanner](./quickstarts/spanner)       | Spanner is used as our globally scalable ACID compliant database. |
| [GenAI LLM](./quickstarts/genai_llm)             | The GenAI LLM service can be configured to deploy [Google Vertex LLMs](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/overview) for Text, Chat, and Code generation. |
| [GenAI Image Gen with OS](./quickstarts/genai_image_gen_os)           | This service deploys an open source stable diffusion model from [Hugging Face](https://huggingface.co/models?sort=trending&search=stable+diffusion). |
| [Vertex ML Training](./quickstarts/vertex_ml_training)         | This code contains an example model training pipeline using tensorflow and [Vertex AI Custom Training](https://cloud.google.com/vertex-ai/docs/training/overview) |
| [Vertex ML Serving](./quickstarts/vertex_ml_serving)         | This service deploys the ML model that was trained in the previous step (or a Tensorflow model that you provide) |
| [Data Pipeline](./quickstarts/data_pipeline)         | This service contains the real-time data pipeline for [Google Dataflow](https://cloud.google.com/dataflow/docs/overview), which accepts real-time events and routes them to backend storage. |


If you'd like to test out the entire framework, then proceed with the following steps (shown below).

## Train ML Model

As part of our framework, provide an example model that you'll train and deploy. The goal is to demonstrate (1) how this model can be trained and deployed in GKE and (2) how the event ingest service is able to make calls to the model in order to get predictions.

Within this step, you'll train a machine learning model using Vertex AI Training and save the model to Google Cloud Storage (GCS). We have provided several examples within the [ml_training](./quickstarts/vertex_ml_training) directory that show different ML techniques and also cover on a variety of use cases. If you're looking for a "getting started" deployment, then you can reference the [ml_training/starter](./quickstarts/vertex_ml_training/starter) directory. 

<br>

## Deploy Kubernetes Services

In this step, you'll build all of the containers required for the deployment. Once successfully built, these containerized services will be deployed to a GKE Autopilot cluster.

NOTE: Make sure to run the [setup.sh](setup.sh) prior to running the following commands if you have not already done so.

1. Build the "Event Ingest" service. The event ingest service is responsible for receiving and routing all game telemetry data from our game servers. The event ingest service is also resposible for sending data and ML results back to the game servers.

    ```sh
    # Build the event ingest container
    cd $PROJECT_ROOT/src/event_ingest
    ./cloudbuild_trigger.sh
    ```

2. Build the "ML Serving" service. The ML serviving service contains the ML model that you trained in the prvious step, called "Train ML Model". This service containerizes the train ML model object and optimizes it for low-latency ML serving.

    ```sh
    # Build the ml serving container
    cd $PROJECT_ROOT/src/ml_serving/
    ./cloudbuild_trigger.sh
    ```

3. Build the GenAI Image Generation (using Stable Diffusion) service. This service will enable in-game 2d image generation specifically for billboards. 

    ```sh
    # Build the genai 2d image generation service
    cd $PROJECT_ROOT/src/genai_image_gen_os/
    ./cloudbuild_trigger.sh
    ```

5. Build the LLM serving service that interacts with the Vertex AI bison model. This service will enable LLM interactions either for (1) in-game prompts and/or (2) developer code generation.

    ```sh
    # Build the LLM serving service
    cd $PROJECT_ROOT/src/genai_llm/
    ./cloudbuild_trigger.sh
    ```

6. Now that the containers have been build, deploy the kubernetes resources:

    ```sh
    # Deploy Kubernetes resources
    cd $PROJECT_ROOT/src
    ./deploy_to_gke.sh
    ```

    Wait for the services and deployments to complete (takes a couple of minutes).

7. Test the event ingest (game telemetry) endpoint

    ```sh
    cd $PROJECT_ROOT/src

    # Get the IP of the event ingest service running on GKE
    export EVENT_INGEST_IP=$(kubectl get svc event-ingest-service -n game-event-ns -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
    
    # Send test data to the endpoint (this will send dummy data through our event ingest service and hit the ml model in order to get a prediction/score).
    python3 event_ingest/send_tcp_traffic.py --host $EVENT_INGEST_IP --port 80
    ```

<br>

---

## Contributing

The entire repo can be cloned and used as-is, or in many cases you may choose to fork this repo and keep the code base that is most useful and relevant for your use case. If you'd like to contribute, then more info can be found witin our [contributing guide](./CONTRIBUTING.md).

---

## Licence

Apache 2.0
