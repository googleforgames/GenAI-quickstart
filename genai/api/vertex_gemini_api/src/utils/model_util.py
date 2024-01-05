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

import sys
import json
import requests
import vertexai
import logging
from vertexai.preview.generative_models import GenerativeModel, GenerationConfig


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)


class GCP_GenAI_Gemini:

    def __init__(self, GCP_PROJECT_ID, GCP_REGION,  MODEL_TYPE):
        if GCP_PROJECT_ID=="":
            logging.warning(f'GCP_PROJECT_ID ENV variable is empty. Be sure to set the GCP_PROJECT_ID ENV variable.')
        
        if GCP_REGION=="":
            logging.warning(f'GCP_REGION ENV variable is empty. Be sure to set the GCP_REGION ENV variable.')

        if MODEL_TYPE=="":
            logging.warning(f'MODEL_TYPE ENV variable is empty. Be sure to set the MODEL_TYPE ENV variable.') 
        
        self.GCP_PROJECT_ID = GCP_PROJECT_ID
        self.GCP_REGION = GCP_REGION
        self.MODEL_TYPE = MODEL_TYPE
        self.pretrained_model = f'{MODEL_TYPE.lower()}'

        self.vertexai = vertexai.init(project=GCP_PROJECT_ID, location=GCP_REGION)
        
        if MODEL_TYPE.lower() == 'gemini-pro':
            self.model = GenerativeModel(self.pretrained_model)
        else:
            # MODEL_TYPE can be "gemini-pro"
            logging.error(f'No MODEL_TYPE specified or MODEL_TYPE is incorrect. Expecting MODEL_TYPE ENV var of "gemini-pro"')
            sys.exit()

    def call_llm(self, 
        prompt,
        temperature=0.5, 
        max_output_tokens=1024, 
        top_p=0.8,
        top_k=40, 
        stop_sequences=None, 
        safety_settings=None,
        ):
        
        if self.MODEL_TYPE.lower() == 'gemini-pro':
            '''
                The Vertex AI Gemini API supports multimodal prompts as input and ouputs text or code.
                https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini
                https://cloud.google.com/vertex-ai/docs/generative-ai/multimodal/send-chat-prompts-gemini
            '''
            try:
                response = self.model.generate_content(
                    contents=prompt,
                    generation_config=GenerationConfig(
                        temperature=temperature,
                        top_p=top_p,
                        top_k=top_k,
                        candidate_count=1,
                        max_output_tokens=max_output_tokens,
                        stop_sequences=stop_sequences,
                    ),
                    safety_settings=safety_settings
                )

                return response
            except Exception as e:
                logging.exception(f'At call_llm for gemini-pro. {e}')
                return ''
