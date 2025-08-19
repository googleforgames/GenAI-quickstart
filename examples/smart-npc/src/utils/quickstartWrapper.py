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
"""
GenAI-Quickstart Chat API Wrapper.
"""

import os
import json
import requests
import logging
from vertexai.generative_models import GenerationResponse, Content

class quick_start_wrapper():
    """
    Google for Games GenAI-Quickstart Chat API Wrapper.
    The class aims to provide Google Unified interface to the GenAI-Quickstart client.
    """
    def __init__(self, model_name:str,
                 system_instruction:str):
        """
        Initialize the wrapper
        Args:
            model_name(str): Name of the model, should be "Gemini"
            system_instruction: System prompt.
            host(str): GenAI-Quickstart chat api host url. ex, http://api.genai.svc
        """
        self.system_instruction = system_instruction
        self.model_name = model_name
        self.host = "http://genai-api.genai.svc/genai/chat/"
        self.history = []
        self.logger = logging.getLogger("smart-npc")
        self.logger.setLevel(logging.DEBUG)

    def start_chat(self, history:list[dict]) -> any:
        """
        Start a chat.
        Args:
            history(list[dict]): conversation history
        Retuns:
            Response from the LLM
        """
        self.history = history if history is not None else []
        return self

    def send_message(self,
                     query:list[str],
                     generation_config:dict=None,
                     safety_settings:dict=None) -> GenerationResponse:
        """
        Send message to the chat model.
        Args:
            query(str): User's input
            generation_config(dict): generation config.
            safety_settings(dict): safety settings.
        Retuns:
            LLM response.
        """
        self.logger.info(
f"""
=====================
* System Instruction:
{self.system_instruction}
* Final Player Input:
{query[0]}
=====================
"""
        )
        request = {
            "prompt": query[0],
            "max_output_tokens": 8192,
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "message_history": None, # self.history if self.history is not None and self.history != [] else None,
            "context": self.system_instruction
        }
        try:
            response = requests.post(self.host, json = request, timeout=30)
            self.logger.info({"message": f"quickStart API elapsed: {response.elapsed.total_seconds()} seconds."})
        except Exception as e:
            self.logger.error(f"* Request:{request}")
            self.logger.error(f"* Exception:{e}")
            raise e

        self.logger.info(f"""******
response:
{response}

Response.Text:
{response.text}
******")
""")
        if self.history is None:
            self.history = []
        if response.status_code == 200: # response.text != "{}":
            answer = {
                "candidates": [
                    {
                        "content":{
                            "parts":[
                                {"text":json.loads(response.text.lstrip("```json").rstrip("```"))}
                            ]
                        }
                    }
                ]
            }
            self.logger.info(f"---> ANSWER <---\n{answer}")
            resp = GenerationResponse.from_dict(answer)
            # resp.candidates[0].content.parts[0].text = json.loads(resp.candidates[0].content.parts[0].text)
            self.history.append(
                {
                    "role":"user",
                    "parts":[{"text": q} for q in query]
                }
            )
            self.history.append(
                {
                    "role":"model",
                    "parts":[
                        {"text":response.text}
                    ]
                }
            )
            return resp
        else:
            self.logger.error(f"error send_message:response.status_code={response.status_code}")
            return None
