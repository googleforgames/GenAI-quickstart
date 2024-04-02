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
from vertexai.language_models import TextGenerationModel, ChatModel, CodeGenerationModel, CodeChatModel, InputOutputTextPair
from vertexai.preview.vision_models import Image, ImageGenerationModel


class Google_Cloud_GenAI:

    def __init__(self, GCP_PROJECT_ID, GCP_REGION,  MODEL_TYPE):
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
        
        if MODEL_TYPE.lower() == 'text-bison':
            self.model = TextGenerationModel.from_pretrained(self.pretrained_model)
        elif MODEL_TYPE.lower() == 'chat-bison':
            self.model = ChatModel.from_pretrained(self.pretrained_model)
        elif MODEL_TYPE.lower() == 'code-bison':
            self.model = CodeGenerationModel.from_pretrained(self.pretrained_model)
        elif MODEL_TYPE.lower() == 'codechat-bison':
            self.model = CodeChatModel.from_pretrained(self.pretrained_model)
        else:
            # MODEL_TYPE can be "text-bison", "chat-bison", "code-bison", or "codechat-bison"
            print(f'[ ERROR ] No MODEL_TYPE specified or MODEL_TYPE is incorrect. Expecting MODEL_TYPE ENV var of "text-bison", "chat-bison", "code-bison", or "codechat-bison".')
            sys.exit()

    def call_llm(self, prompt, temperature=0.2, max_output_tokens=256, top_p=0.8, top_k=40, context='', chat_examples=[], code_suffix=''):
        if self.MODEL_TYPE.lower() == 'text-bison':
            try:
                parameters = {
                    "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
                    "max_output_tokens": max_output_tokens, # Token limit determines the maximum amount of text output.
                    "top_p": top_p,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
                    "top_k": top_k,  # A top_k of 1 means the selected token is the most probable among all tokens.
                }

                response = self.model.predict(
                    prompt,
                    **parameters,
                )
                return response
            except Exception as e:
                print(f'[ EXCEPTION ] At call_llm for text-bison. {e}')
                return ''
        
        elif self.MODEL_TYPE.lower() == 'chat-bison':
            try:
                '''
                examples=[
                    InputOutputTextPair(
                        input_text="Who do you work for?",
                        output_text="I work for Ned.",
                    ),
                    InputOutputTextPair(
                        input_text="What do I like?",
                        output_text="Ned likes watching movies.",
                    ),
                ]
                '''

                chat = self.model.start_chat(
                    context=context,
                    examples=chat_examples,
                    temperature=temperature,
                    max_output_tokens=max_output_tokens,
                    top_p=top_p,
                    top_k=top_k
                )

                response = chat.send_message(prompt)
                return response
            except Exception as e:
                print(f'[ EXCEPTION ] At call_chat for chat-bison. {e}')
                return ''
        
        elif self.MODEL_TYPE.lower() == 'code-bison':
            '''A language model that generates code.'''
            try:
                response = self.model.predict(prefix=prompt, temperature=temperature, max_output_tokens=max_output_tokens, suffix=code_suffix)
                return response
            except Exception as e:
                print(f'[ EXCEPTION ] At call_chat for codechat-bison. {e}')
                return ''        
        
        elif self.MODEL_TYPE.lower() == 'codechat-bison':
            '''CodeChatModel represents a model that is capable of completing code.'''
            try:
                code_chat = self.model.start_chat(
                    max_output_tokens=max_output_tokens,
                    temperature=temperature,
                )

                response = code_chat.send_message(prompt)
                return response
            except Exception as e:
                print(f'[ EXCEPTION ] At call_chat for codechat-bison. {e}')
                return ''


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
        self.model = ImageGenerationModel.from_pretrained("imagegeneration@005")
