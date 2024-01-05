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
from utils.model_util import GCP_GenAI_Gemini
import io
import os, sys
import json
import requests
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)

app = FastAPI(
    redoc_url=None,
    title="API for the Vertex AI Gemini LLM",
    description="GenAI service that may contain business logic, data processing steps, and makes calls to the Google Cloud Gemini LLM",
    version="0.0.1",
)

def get_gcp_metadata():
    metadata_server = "http://metadata.google.internal"
    headers = {"Metadata-Flavor": "Google"}

    # Get Project ID
    project_id_url = f"{metadata_server}/computeMetadata/v1/project/project-id"
    project_id_response = requests.get(project_id_url, headers=headers)
    project_id = project_id_response.text if project_id_response.status_code == 200 else "Unavailable"

    # Get GCP Zone
    zone_url = f"{metadata_server}/computeMetadata/v1/instance/zone"
    zone_response = requests.get(zone_url, headers=headers)
    zone = zone_response.text.split('/')[-1] if zone_response.status_code == 200 else "Unavailable"

    # Extract GCP Region
    region = '-'.join(zone.split('-')[:-1])

    return project_id, region, zone

GCP_PROJECT_ID, GCP_REGION, GCP_ZONE = get_gcp_metadata()
logging.debug(f'GCP_PROJECT_ID: {GCP_PROJECT_ID}')
logging.debug(f'GCP_REGION:     {GCP_REGION}')
logging.debug(f'GCP_ZONE:       {GCP_ZONE}')

# Initialize Vertex LLM Model
model = GCP_GenAI_Gemini(GCP_PROJECT_ID=GCP_PROJECT_ID, GCP_REGION=GCP_REGION,  MODEL_TYPE='gemini-pro')

headers = {"Content-Type": "application/json"}

class Payload_Vertex_Gemini(BaseModel):
    prompt: str
    max_output_tokens: int | None = 1024
    temperature: float | None = 0.4
    top_p: float | None = 0.8
    top_k: int | None = 40
    stop_sequences: list | None = None
    safety_settings: dict | None = None


# Routes


@app.get("/genai_health", include_in_schema=False)
async def health_check():
    return {'status': 'ok'}


@app.post("/")
def vertex_gemini_llm(payload: Payload_Vertex_Gemini):
    try:
        request_payload = {
            'prompt': payload.prompt,
            'max_output_tokens': payload.max_output_tokens,
            'temperature': payload.temperature,
            'top_p': payload.top_p,
            'top_k': payload.top_k,
            'stop_sequences': payload.stop_sequences,
            'safety_settings': payload.safety_settings,
        }
        response = model.call_llm(**request_payload)
        return response.text
    except Exception as e:
        print(f'EXCEPTION: {e}')
        return {}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7777)




