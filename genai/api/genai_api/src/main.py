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

import os, sys
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse, JSONResponse
import io
import json
import requests


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)


tags_metadata = [
    {
        "name": "text",
        "description": "The Text endpoint routes to a general purpose llm that can handle Q&A, summarization, classifcation, extraction of information, etc.",
    },
    {
        "name": "chat",
        "description": "The Chat endpoint routes to a multi-turn chat service, which maintains the history of a conversation and then uses that history as the context for responses.",
    },
    {
        "name": "code",
        "description": "The Code endpoint routes to an LLM optimized for code generation and general purpose coding support.",
    },
    {
        "name": "image",
        "description": "The Image endpoint routes to a service that can be used to generate 2D images based on a text prompt.",
    },
]


app = FastAPI(
    docs_url='/genai_docs', 
    redoc_url=None,
    title="GenAI Quickstart APIs",
    description="Core APIs for the GenAI Quickstart for Gaming",
    version="0.2.0",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata,
)


GENAI_GEMINI_ENDPOINT= os.environ['GENAI_GEMINI_ENDPOINT'] 
GENAI_TEXT_ENDPOINT  = os.environ['GENAI_TEXT_ENDPOINT']
GENAI_CHAT_ENDPOINT  = os.environ['GENAI_CHAT_ENDPOINT']
GENAI_CODE_ENDPOINT  = os.environ['GENAI_CODE_ENDPOINT']
GENAI_IMAGE_ENDPOINT = os.environ['GENAI_IMAGE_ENDPOINT']


headers = {"Content-Type": "application/json"}


class Payload_Vertex_Gemini(BaseModel):
    prompt: str
    max_output_tokens: int | None = 1024
    temperature: float | None = 0.4
    top_p: float | None = 0.8
    top_k: int | None = 40
    stop_sequences: list | None = None
    safety_settings: dict | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "prompt": "Can you describe a new level that you would add to Super Mario Bros",
                    "max_output_tokens": 1024,
                    "temperature": 0.2,
                    "top_p": 0.8,
                    "top_k": 40,
                }
            ]
        }
    }



class Payload_Chat(BaseModel):
    prompt: str
    context: str | None = ''
    max_output_tokens: int | None = 1024
    temperature: float | None = 0.2
    top_p: float | None = 0.8
    top_k: int | None = 40

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "prompt": "What is your favorite thing to do?",
                    "context": "You are Mario from Super Mario Bros.",
                    "max_output_tokens": 1024,
                    "temperature": 0.2,
                    "top_p": 0.8,
                    "top_k": 40,
                }
            ]
        }
    }


class Payload_Text(BaseModel):
    prompt: str
    max_output_tokens: int | None = 1024
    temperature: float | None = 0.2
    top_p: float | None = 0.8
    top_k: int | None = 40

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "prompt": "Can you describe the final level within Super Mario Bros.",
                    "max_output_tokens": 1024,
                    "temperature": 0.2,
                    "top_p": 0.8,
                    "top_k": 40,
                }
            ]
        }
    }


class Payload_Code(BaseModel):
    prompt: str
    max_output_tokens: int | None = 1024
    temperature: float | None = 0.2
    top_p: float | None = 0.8
    top_k: int | None = 40

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "prompt": "Can you write a python function that sums two floats?",
                    "max_output_tokens": 1024,
                    "temperature": 0.2,
                    "top_p": 0.8,
                    "top_k": 40,
                }
            ]
        }
    }


class Payload_Image(BaseModel):
    prompt: str
    number_of_images: int | None = 1
    seed: int | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "prompt": "cartoon image of Mario and the Princess with the castle in the background",
                    "number_of_images": 1,
                    "seed": 12345,
                }
            ]
        }
    }


# Routes


@app.get("/genai_health", include_in_schema=False)
async def health_check():
    return {'status': 'ok'}


@app.post("/genai", tags=["gemini-pro"])
def genai_gemini(payload: Payload_Vertex_Gemini):
    '''
    Google GenAI Gemini Multimodal model
    '''
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
        response = requests.post(f'{GENAI_GEMINI_ENDPOINT}', headers=headers, json=request_payload)
        logging.debug(f'request_payload: {request_payload}')
        return json.loads(response.content)
    except Exception as e:
        logging.exception(f'At /genai. {e}')
        return JSONResponse(
            status_code=400,
            content={'status': 'exception calling google genai gemini endpoint'},
        )


@app.post("/genai/text", tags=["text"])
def genai_text(payload: Payload_Text):
    try:
        request_payload = {
            'prompt': payload.prompt, 
            'max_output_tokens': payload.max_output_tokens,
            'temperature': payload.temperature,
            'top_p': payload.top_p,
            'top_k': payload.top_k,
        }
        response = requests.post(f'{GENAI_TEXT_ENDPOINT}', headers=headers, json=request_payload)
        logging.debug(f'request_payload: {request_payload}')
        return json.loads(response.content)
    except Exception as e:
        logging.exception(f'At /genai/text. {e}')
        return JSONResponse(
            status_code=400,
            content={'status': 'exception calling endpoint'},
        )


@app.post("/genai/chat", tags=["chat"])
def genai_chat(payload: Payload_Chat):
    try:
        request_payload = {
            'prompt': payload.prompt,
            'context': payload.context,
            'max_output_tokens': payload.max_output_tokens,
            'temperature': payload.temperature,
            'top_p': payload.top_p,
            'top_k': payload.top_k,
        }
        logging.debug(f'request_payload: {request_payload}')
        response = requests.post(f'{GENAI_CHAT_ENDPOINT}', headers=headers, json=request_payload)
        return json.loads(response.content)
    except Exception as e:
        logging.exception(f'At /genai/chat. {e}')
        return JSONResponse(
            status_code=400,
            content={'status': 'exception calling endpoint'},
        )


@app.post("/genai/code", tags=["code"])
def genai_code(payload: Payload_Code):
    try:
        request_payload = {
            'prompt': payload.prompt, 
            'max_output_tokens': payload.max_output_tokens,
            'temperature': payload.temperature,
            'top_p': payload.top_p,
            'top_k': payload.top_k,
        }
        logging.debug(f'request_payload: {request_payload}')
        response = requests.post(f'{GENAI_CODE_ENDPOINT}', headers=headers, json=request_payload)
        return json.loads(response.content)
    except Exception as e:
        logging.exception(f'At /vertex_llm_code. {e}')
        return JSONResponse(
            status_code=400,
            content={'status': 'exception calling endpoint.'},
        )


@app.post("/genai/image", tags=["image"])
def genai_image(payload: Payload_Image):
    try:
        request_payload = {
            'prompt': payload.prompt, 
            'number_of_images': payload.number_of_images,
            'seed': payload.seed,
        }
        logging.debug(f'request_payload: {request_payload}')
        images = requests.post(f'{GENAI_IMAGE_ENDPOINT}', headers=headers, json=request_payload)
        # Return the first image of the list
        return StreamingResponse(io.BytesIO(images.content), media_type="image/png")
    except Exception as e:
        logging.exception(f'At /genai/image. {e}')
        return JSONResponse(
            status_code=400,
            content={'status': 'exception calling endpoint'},
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7777)

