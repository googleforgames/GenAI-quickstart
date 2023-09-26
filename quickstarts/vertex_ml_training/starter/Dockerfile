FROM us-docker.pkg.dev/vertex-ai/training/tf-cpu.2-8:latest

WORKDIR /app

ARG GCS_MODEL_PATH
ENV GCS_MODEL_PATH=$GCS_MODEL_PATH

COPY model_training.py ./model_training.py

# Sets up the entry point to invoke the trainer.
ENTRYPOINT ["python3", "/app/model_training.py"]
