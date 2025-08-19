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

from google import genai
from google.genai import types
from vertexai.language_models import TextGenerationModel, ChatModel, CodeGenerationModel, CodeChatModel, InputOutputTextPair
from vertexai.preview.vision_models import Image, ImageGenerationModel
from vertexai.generative_models import GenerativeModel

class Google_Cloud_GenAI:

    def __init__(self, GCP_PROJECT_ID, GCP_REGION,  MODEL_TYPE, system_prompt:str=""):
        if GCP_PROJECT_ID=="":
            print(f'[ WARNING ] GCP_PROJECT_ID ENV variable is empty. Be sure to set the GCP_PROJECT_ID ENV variable.')

        if GCP_REGION=="":
            print(f'[ WARNING ] GCP_REGION ENV variable is empty. Be sure to set the GCP_REGION ENV variable.')

        if MODEL_TYPE=="":
            print(f'[ WARNING ] MODEL_TYPE ENV variable is empty. Be sure to set the MODEL_TYPE ENV variable.')

        self.GCP_PROJECT_ID = GCP_PROJECT_ID
        self.GCP_REGION = GCP_REGION
        self.MODEL_TYPE = MODEL_TYPE
        self.pretrained_model = f'{MODEL_TYPE.lower()}@001'

        self.vertexai = vertexai.init(project=GCP_PROJECT_ID, location=GCP_REGION)

        if MODEL_TYPE.lower() == 'gemini':
            self.model = None
        elif MODEL_TYPE.lower() == 'gemini-2.0':
            self.model = None
        else:
            print(f'[ ERROR ] No MODEL_TYPE specified or MODEL_TYPE ({MODEL_TYPE}) is incorrect. Expecting MODEL_TYPE ENV var of "text-bison", "chat-bison", "code-bison", or "codechat-bison".')
            sys.exit()

    def call_llm(self, prompt, temperature=0.2, max_output_tokens=256, top_p=0.8, top_k=40, context='', chat_examples=[], message_history=[], code_suffix=''):
        if self.MODEL_TYPE.lower() == "gemini-2.0" or self.MODEL_TYPE.lower() =="gemini":
            client = genai.Client(
                vertexai=True,
                project=self.GCP_PROJECT_ID,
                location=self.GCP_REGION
            )
            model_name = "gemini-2.0-flash-exp"
            generate_content_config = types.GenerateContentConfig(
                temperature = 1,
                top_p = 0.95,
                max_output_tokens = 8192,
                response_modalities = ["TEXT"],
                safety_settings = [
                    types.SafetySetting(
                        category="HARM_CATEGORY_HATE_SPEECH",
                        threshold="OFF"
                    ),
                    types.SafetySetting(
                        category="HARM_CATEGORY_DANGEROUS_CONTENT",
                        threshold="OFF"
                        ),
                    types.SafetySetting(
                        category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        threshold="OFF"
                        ),
                    types.SafetySetting(
                        category="HARM_CATEGORY_HARASSMENT",
                        threshold="OFF"
                    )],
                system_instruction=[types.Part.from_text(context)]
            )
            prediction_result = ""
            if message_history is None:
                message_history = []

            message_history.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(prompt)
                    ]
                )
            )
            conv_logs = [
                types.Content(
                    role=q.role,
                    parts = [
                        types.Part.from_text(c.text) for c in q.parts
                    ]
                ) for q in message_history]
            for chunk in client.models.generate_content_stream(
                    model = model_name,
                    contents = conv_logs,
                    config = generate_content_config,
                ):
                if chunk.candidates is not None and len(chunk.candidates) > 0:
                    prediction_result = prediction_result + chunk.candidates[0].content.parts[0].text

            print(f"Gemini-2.0-Flash::prediction_result={prediction_result}")
            return prediction_result
        else:
            print(f"[Error]Invalid Model Type:{self.MODEL_TYPE}")

class Google_Cloud_Imagen:
    '''
    https://cloud.google.com/vertex-ai/docs/generative-ai/image/overview
    '''

    def __init__(self, GCP_PROJECT_ID, GCP_REGION):
        if GCP_PROJECT_ID=="":
            print(f'[ WARNING ] GCP_PROJECT_ID ENV variable is empty. Be sure to set the GCP_PROJECT_ID ENV variable.')

        if GCP_REGION=="":
            print(f'[ WARNING ] GCP_REGION ENV variable is empty. Be sure to set the GCP_REGION ENV variable.')

        self.GCP_PROJECT_ID = GCP_PROJECT_ID
        self.GCP_REGION = GCP_REGION

        self.vertexai = vertexai.init(project=GCP_PROJECT_ID, location=GCP_REGION)
        self.model = ImageGenerationModel.from_pretrained("imagegeneration@002")
