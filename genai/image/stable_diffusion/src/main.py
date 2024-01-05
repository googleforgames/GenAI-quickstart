# Copyright 2024 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fastapi import FastAPI, Response
from pydantic import BaseModel
import requests
import os
import json
from utils.model_util import Stable_Diffusion
import logging
from logging.config import dictConfig
from utils.log_conf import log_config


# Initialize Logging
dictConfig(log_config)
logger = logging.getLogger('app-logger')


# Initialize the app
app = FastAPI(
    redoc_url=None,
    title="Stable Diffusion LLM Service",
    description="This service deploys an open source stable diffusion model from Hugging Face.",
    version="0.0.1",
)


# Get ENV Variables
# Model Type should reference a image generation model from HuggingFace.
# https://huggingface.co/models
# Example 1: MODEL_TYPE = 'dreamlike-art/dreamlike-photoreal-2.0'
# Example 2: MODEL_TYPE = 'runwayml/stable-diffusion-v1-5'
MODEL_TYPE = os.environ['MODEL_TYPE']


# Initialize model object
model = Stable_Diffusion(model_type=MODEL_TYPE)


# Set fastapi payload input structure for POST
class Payload(BaseModel):
    prompt: str


# Routes


@app.get("/genai_health", include_in_schema=False)
async def health_check():
    return {'status': 'ok'}


@app.get("/")
async def generate_image_get(prompt: str):
    try:
        img = model.get_image(prompt)
        return Response(content=img, media_type="image/png")

    except Exception as e:
        logger.warning(f'[ EXCEPTION ] {e}')
        return {"error": "Invalid text prompt"}, 400


@app.post("/")
async def generate_image_post(payload: Payload):
    try:
        img = model.get_image(payload.prompt)
        return Response(content=img, media_type="image/png")

    except Exception as e:
        logger.warning(f'[ EXCEPTION ] {e}')
        return {"error": "Invalid text prompt"}, 400


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7777)

