# Quickstart for Vertex ML Training

This quickstart provides a self-contained set of instructions for training and deploying a basic ML model using Google Cloud Vertex AI. We're providing this code and set of instructions as a reference and a potential starting point, so feel free to modify it to suit your specific needs.  

---

### Prerequisites

Prior to launching the quickstart, ensure that you have successfully ran the [setup.sh](../../setup.sh) (`. setup.sh`) within the root directory of this project. This setup file will set your environment variables (which can be modified) and it will also check that your enviornment has the required services such as Terraform, the Google Cloud SDK, and any other dependencies required for this deployment.

After running the `setup.sh`, verify that a .env file has been created within your project root directory and that the `PROJECT_ROOT` env variable is set to the base path for this repo.

If all of that looks good, then you can move on to the next step.

### Step 1 - Deploy the GCP infrastructure

Before you can deploy the services within this quickstart, you will need to provision the GCP resources which will setup your Artifact Registry, Database (if needed), Google Cloud Storage buckets, etc. Feel free to modify the deployment as needed based on your desired infrastructure requirements. To provision your GCP resource, follow the [README](../../infra/README.md) located within the [infra](../../infra/) directory.

### Step 2 - Train ML Model 

In this step, you'll train a machine learning model using Vertex AI Training and save the model to Google Cloud Storage (GCS). We have provided several examples within this directory that show different ML techniques and also cover on a variety of use cases. If you're looking for a "getting started" deployment, then you can reference the [./starter](./starter) directory. 


The following command will train an ML model based on this example [ML training code](./starter/model_training.py). When the command (below) is ran, it'll containerize the ML training code, send it to vertex AI, and then the saved model assets will be stored in GCS at the location that specified within the [.env](../../.env), which is created when running the [setup.sh](../../setup.sh). Run this command to train the ML model.

```sh
$PROJECT_ROOT/quickstarts/vertex_ml_training/starter/cloudbuild_trigger.sh
```

### Step 3. Validate that the model trained successfully

Vertex AI will take several minutes to train your ML model. The output will be stored in the GCS location specified in the .env. The Custom Training job details will also be available within Vertex AI Training. This model will be deployed as part of the next step, which is called "Deploy Kubernetes Services". Once training is complete, your model should be available at this GCS location:

```sh
# Show GCS path where the ML model should be saved.
echo $GCS_MODEL_PATH

# Print the contents of the GCS path, which should contained the saved model assets.
gsutil ls $GCS_MODEL_PATH

# You can also view Vertex AI Custom Training Jobs using this gcloud command,
# or you could view the Vertex AI train job within the GCP Console UI.
gcloud ai custom-jobs list --region $GCP_REGION
```
