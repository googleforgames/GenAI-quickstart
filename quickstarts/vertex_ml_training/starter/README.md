# Getting Started - ML Training

The contents within this directory contain a "getting started" structure for ML training on Vertex AI using custom containers. Below, you will find instruction for running this training job on Vertex.

## Setup

1. Review the contents of the ML Training code. This example code, writting in python using tensorflow, is meant provided as a reference that can be modified in order to meet your specific training requirements.

    [Sample Code (as a Notebook)](./model_training.ipynb)
    [Sample Code (as a raw .py)](./model_training.py)

2. Make sure to run the [setup.sh](../../setup.sh) in the root of the udp repo, and also check that the variables contained within .env match your GCP project name and meet your naming conventions. 

    ```
    # Run this command to initialize the environment and set the environment variables.
    # The setup.sh is located in the root of the upd directory.
    source ../../setup.sh
    ```

3. Deploy the Training Job using Cloud Build

    ```
    ./cloudbuild_trigger.sh
    ```

    Once this job completes, your ML model should be trained. The containerized model assets should exists within Google Artifict Repo, specifically in the "udp-repo" artifact repo if you used all of the default naming conventions, and also in a Google Cloud Storage bucketed named gs://<your_gcp_project_id>-models.
