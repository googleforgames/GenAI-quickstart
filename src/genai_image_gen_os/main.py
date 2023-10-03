# Copyright 2023 Google LLC All Rights Reserved.
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

# Local Dev: uvicorn main:app --host 0.0.0.0 --port 7777

from fastapi import FastAPI, Response
from pydantic import BaseModel
import requests
import os
import json
from model_util import Stable_Diffusion


app = FastAPI()


GCP_PROJECT_ID = os.environ['GCP_PROJECT_ID']
# Model Type should reference a image generation model from HuggingFace.
# https://huggingface.co/models
# Example 1: MODEL_TYPE = 'dreamlike-art/dreamlike-photoreal-2.0'
# Example 2: MODEL_TYPE = 'runwayml/stable-diffusion-v1-5'
MODEL_TYPE = os.environ['MODEL_TYPE']


model = Stable_Diffusion(model_type=MODEL_TYPE)
#model.load_model()


class Payload(BaseModel):
    prompt: str


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.get("/generate_img")
async def generate_img_get(prompt: str):
    try:
        img = model.get_image(prompt)
        return Response(content=img, media_type="image/png")

    except Exception as e:
        print(f'[ EXCEPTION ] {e}')
        return {"error": "Invalid text prompt"}, 400


@app.post("/generate_img")
async def generate_img_post(payload: Payload):
    try:
        img = model.get_image(payload.prompt)
        return Response(content=img, media_type="image/png")

    except Exception as e:
        print(f'[ EXCEPTION ] {e}')
        return {"error": "Invalid text prompt"}, 400

