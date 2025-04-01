# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""LLM operation help class

Wrapper of LLM operations.
"""

import os
import json
import logging

from utils.const import USE_QUICK_START
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
from vertexai.preview import generative_models
from vertexai.generative_models import GenerativeModel
from utils.quickstartWrapper import quick_start_wrapper

EMBEDDING_MODEL_NAME = "text-multilingual-embedding-002"
TEXT_GENERATION_MODEL_NAME = "gemini-1.5-flash-001"
GEMINI_GENERATION_MODEL_NAME = "gemini-1.5-pro-001"
FLASH_MODEL_NAME = "gemini-1.5-flash-002"
PRO_MODEL_NAME= "gemini-1.5-pro-002"

logger = logging.getLogger("smart-npc")
logger.setLevel(logging.DEBUG)

def text_embedding(
    task_type: str,
    text: str,
    title: str = "",
    model_name: str = EMBEDDING_MODEL_NAME
  ) -> list:
    """Generate text embedding with a Large Language Model.

    Args:
    task_type (str): Task type,
    Please see:
    https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/task-types#supported_task_types

    text (str): input text
    title (str): Optional title of the input text
    model_name (str): Defaults to text-multilingual-embedding-002

    Returns:
        Embeddings
    """
    model = TextEmbeddingModel.from_pretrained(model_name)
    if task_type == "" or task_type is None:
        logger.info("[Info]NO Emgedding Task Type")
        embeddings = model.get_embeddings([text])
    else:
        text_embedding_input = TextEmbeddingInput(
            task_type=task_type, title=title, text=text)
        embeddings = model.get_embeddings([text_embedding_input])
    return embeddings[0].values

def ask_llm(prompt:str,
            model_name = TEXT_GENERATION_MODEL_NAME,
            generation_configuration=None,
            safety_configuration=None) -> str:
    """Invoke Language Model.

    Args:
        model_name (str): Model name, defaults to "gemini-1.5-flash-001"
        generation_configuration (dict): Generation config
        safety_configuration (dict): Safty config

    Returns:
        Large Language Model prediction results.
    """
    if generation_configuration is None:
        generation_configuration = {
                "max_output_tokens": 8192,
                "temperature": 1,
                "top_p": 0.95,
            }
    if safety_configuration is None:
        safety_configuration = {
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_NONE,  # pylint: disable=line-too-long
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_NONE,  # pylint: disable=line-too-long
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_NONE,  # pylint: disable=line-too-long
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_NONE,  # pylint: disable=line-too-long
        }

    if not USE_QUICK_START:
        model = GenerativeModel(
            FLASH_MODEL_NAME,
            system_instruction=[""]
        )
    else:
        model = quick_start_wrapper(
                model_name=FLASH_MODEL_NAME,
                system_instruction="",
        )

    responses = model.generate_content(
        [prompt],
        generation_config=generation_configuration,
        safety_settings=safety_configuration,
        stream=True,
    )
    result_text = ""
    for response in responses:
        result_text += response.text
    if "```" in result_text:
        result_text = result_text.replace("```json", "").replace("```html", "")
        result_text = result_text[0:result_text.index("```") - 1]
    return result_text
