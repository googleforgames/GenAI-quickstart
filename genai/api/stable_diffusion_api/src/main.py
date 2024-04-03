# Copyright 2024 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import io
import os
import json
import requests


app = FastAPI(
    redoc_url=None,
    title="API for Open Source Stable Diffusion",
    description="Contains business logic, data processing, and routing to the open source Stable Diffusion service.",
    version="0.0.1",
)


# Get ENV Variables
STABLE_DIFFUSION_ENDPOINT = os.environ['STABLE_DIFFUSION_ENDPOINT']


headers = {"Content-Type": "application/json"}

class Payload_StableDiffusion(BaseModel):
    prompt: str
    number_of_images: int | None = 1
    seed: int | None = None


# Routes


@app.get("/genai_health", include_in_schema=False)
async def health_check():
    return {'status': 'ok'}


@app.get("/")
def image_gen_open_source_x_get(
        prompt: str,
        number_of_images: int = 1,
        seed: int = None,
    ):
    try:
        if number_of_images > 1 or seed:
            print('parameters seed and number_of_images not supported, ignored')
        request_payload = {
            'prompt': prompt,
        }
        req = requests.post(STABLE_DIFFUSION_ENDPOINT, headers=headers, json=request_payload)
        return StreamingResponse(io.BytesIO(req.content), media_type="image/png")
    except Exception as e:
        print(f'EXCEPTION: {e}')
        return {}


@app.post("/")
def image_gen_open_source_x_post(payload: Payload_StableDiffusion):
    try:
        request_payload = {
            'prompt': payload.prompt,
        }
        req = requests.post(STABLE_DIFFUSION_ENDPOINT, headers=headers, json=request_payload)
        return StreamingResponse(io.BytesIO(req.content), media_type="image/png")
    except Exception as e:
        print(f'EXCEPTION: {e}')
        return {}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7777)

