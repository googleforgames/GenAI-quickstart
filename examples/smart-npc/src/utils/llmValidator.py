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

import os

from models.prompt import PromptRetrievalResponse
from utils.promptManager import PromptManager
from utils.llm import ask_llm

"""
LLM prediction validator
"""
class LLMValidator():
    """
    Helper class to validate LLM predictions.
    """
    def __init__(self, config:dict):
        """
        Initialize the prompt manager helper class.

        Args:
            config (dict): config.toml dict.
        """
        self.prompt_manager = PromptManager(config=config)

    def validate(self,
                 scene_id:str,
                 player_input:str,
                 npc_response:str,
                 npcs:str,
                 conversation_history:list) -> str:

        """
        Validate LLM prediction.
        Args:
            scene_id (str): scene id.
            player_input (str): player input.
            npc_response (str): npc response.
            npcs (str): npcs.
            conversation_history (list): conversation history.
        Returns:
            Validated LLM prediction
        """
        history = ""
        if conversation_history is not None and conversation_history != []:
            for turn in conversation_history:
                history += f"{turn}" + os.linesep

        if history == "":
            history = "N/A"
        try:
            prompt = self.prompt_manager.construct_prompt(
                prompt_id="NPC_CONVERSATION_REVIEW",
                scene_id=scene_id
            )
            prompt.prompt_template = prompt.prompt_template.format(
                NON_PLAYER_CHARACTERS=npcs,
                PLAYER_INPUT=player_input,
                NPC_RESPONSE=npc_response,
                CONVERSATION_HISTORY=conversation_history
            )

            answer = ask_llm(prompt=prompt.prompt_template)
            return answer
        except Exception:
            return npc_response

