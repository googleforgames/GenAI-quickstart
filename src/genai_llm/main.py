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
from model_util import Google_Cloud_GenAI


GCP_PROJECT_ID = os.environ['GCP_PROJECT_ID']
MODEL_TYPE = os.environ['MODEL_TYPE'] # text-bison, chat-bison, code-bison

print(f'[ INFO ] GCP_PROJECT_ID: {GCP_PROJECT_ID}')
print(f'[ INFO ] MODEL_TYPE: {MODEL_TYPE}')

app = FastAPI()


# model_type can be "text-bison", "chat-bison", "code-bison", or "codechat-bison"
model = Google_Cloud_GenAI(GCP_PROJECT_ID, GCP_REGION='us-central1', MODEL_TYPE=MODEL_TYPE)


class Payload(BaseModel):
    prompt: str


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.get("/llm")
async def llm_get(prompt: str):
    try:
        result = model.call_llm(prompt)
        
        # result is a vertex ai obj of type:
        # vertexai.language_models._language_models.TextGenerationResponse
        '''
        # Example Vertex AI TextGenerationResponse:
        {
          "text": "The llm response as text",
          "_prediction_response": [
            [
              {
                "citationMetadata": [
                  {
                    "citations": []
                  }
                ],
                "candidates": [
                  {
                    "content": "The llm response as text",
                    "author": "1"
                  }
                ],
                "safetyAttributes": [
                  {
                    "categories": [
                      "Health"
                    ],
                    "scores": [
                      0.1
                    ],
                    "blocked": false
                  }
                ]
              }
            ],
            "",
            "",
            "",
            null
          ],
          "is_blocked": false,
          "safety_attributes": {
            "Health": 0.1
          }
        }
        '''
        
        return result.text
    except Exception as e:
        print(f'[ EXCEPTION ] {e}')
        return 'exception'


@app.post("/llm")
async def llm_post(payload: Payload):
    try:
        # result is a vertex ai obj of type:
        # vertexai.language_models._language_models.TextGenerationResponse
        result = model.call_llm(payload.prompt)
        return result.text
    except Exception as e:
        print(f'[ EXCEPTION ] {e}')
        return 'exception'
