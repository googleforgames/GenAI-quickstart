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

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from typing import List
import sys
import traceback
import logging

WARMUP_SENTENCE='a warm model is a fast model'

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)

app = FastAPI(
    redoc_url=None,
    title="API for GenAI Embeddings",
    description="Generates Embedding vectors for sentences given the model specified.",
    version="0.0.1",
)

class Payload_Embeddings(BaseModel):
    model: str
    prompts: List[str]


model_cache = {}


def get_model(model_name) -> SentenceTransformer:
    if model_name not in model_cache:
        try:
            model_cache[model_name] = SentenceTransformer(model_name)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f'Model named "{model_name}" not found (browse https://huggingface.co/sentence-transformers for valid models)')
    return model_cache[model_name]


def get_embeddings(model_name: str, prompts: List[str]):
    return get_model(model_name).encode(prompts, show_progress_bar=False, convert_to_tensor=True, normalize_embeddings=True).tolist()


# Routes


@app.get("/genai_health", include_in_schema=False)
async def health_check():
    return {'status': 'ok'}

@app.post("/")
def embeddings(payload: Payload_Embeddings):
    try:
        return {
            'model': payload.model,
            'prompts': payload.prompts,
            'embeddings': get_embeddings(payload.model, payload.prompts),
        }
    except HTTPException as e:
        raise
    except Exception as e:
        traceback.print_exception(e)
        raise HTTPException(status_code=500, detail="Internal error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7777)

