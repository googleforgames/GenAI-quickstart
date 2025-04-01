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

import json
import logging

from utils.const import USE_QUICK_START
from models.scence import (
    NPCSceneConversationRequest,
    NPCSceneConversationResponse,
    Scene
)
from models.prompt import PromptRetrievalResponse
from utils.cacheWrapper import CacheFactory
from utils.database import DataConnection
from utils.cacheWrapper import CacheFactory
from vertexai.preview import generative_models
from vertexai.generative_models import GenerativeModel
from utils.quickstartWrapper import quick_start_wrapper

EMBEDDING_MODEL_NAME = "text-multilingual-embedding-002"
TEXT_GENERATION_MODEL_NAME = "gemini-1.5-flash-001"
GEMINI_GENERATION_MODEL_NAME = "gemini-1.5-pro-001"
FLASH_MODEL_NAME = "gemini-1.5-flash-002"
PRO_MODEL_NAME= "gemini-1.5-pro-002"

"""
Conversation Management Help class
"""
class ConversationManager():
    """
    Helper class for prompt management.
    """
    def __init__(self, config:dict):
        """
        Initialize the prompt manager helper class.

        Args:
            config (dict): config.toml dict.
        """
        self._cache = CacheFactory(config=config).get_cache("conversations")
        self._conversation_history = CacheFactory(config=config).get_cache("conversation_history")
        self._config = config
        self._connection = DataConnection(config=config)
        self._llm_model_name = FLASH_MODEL_NAME

    def __format_conversation_history_cache_key(
        self,
        game_id:str,
        scene_id:str,
        session_id:str,
        player_id:str) -> str:
        """
        Format conversation cache key
        Args:
            game_id (str): game id.
            scene_id (str): scene id.
            session_id (str): session id.
            player_id (str): player id.
        Returns:
            Formatted cache key.
        """
        return f"{game_id}/{scene_id}/{session_id}"

    def __format_conv_example_cache_key(self,
                                        game_id:str,
                                        scene_id:str="default",
                                        example_id:str="default") -> str:
        """
        Format conversation cache key
        Args:
            game_id (str): game id.
            scene_id (str): scene id.
            example_id (str): example id.
        Returns:
            Formatted cache key.
        """
        return f"{game_id}/{scene_id}/{example_id}"

    def get_conv_example(
            self,
            example_id:str="default",
            scene_id:str="default"
        ) -> str:
        """
        Get conversation example.

        Args:
            example_id (str): example id, defaults to "default"
            scene_id (str): scene_id, defaults to "default"

        Returns:
            Conversation Example.
        """
        game_id = self._config["game"]["game_id"]
        key = self.__format_conv_example_cache_key(
                                    game_id=game_id,
                                    scene_id=scene_id,
                                    example_id=example_id)
        example = self._cache.get(key=key)

        if example is None or example == "":
            sql = self._config["sql"]["QUERY_CONV_EXAMPLE"]
            results = self._connection.execute(
                sql = sql,
                sql_params={
                    "example_id":example_id,
                    "scene_id":scene_id,
                    "game_id":game_id
                }
            )
            for result in results:
                example = result[3]
                self._cache.set(key, example)

        return example

    def chat(
            self,
            conversation:NPCSceneConversationRequest,
            prompt:PromptRetrievalResponse
        ):
        """Generate Multi-turn response

        Args:
            conversation (NPCSceneConversationRequest): Player's chat request.
            prompt (PromptRetrievalResponse): Prompt to generate NPC responses.
.
        Returns:
            NPC's response to the player's query and conversation history
        """
        generation_config = {
            "max_output_tokens": 8192,
            "temperature": 1,
            "top_p": 0.95,
        }

        safety_settings = {
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_NONE,  # pylint: disable=line-too-long
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_NONE,  # pylint: disable=line-too-long
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_NONE,  # pylint: disable=line-too-long
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_NONE,  # pylint: disable=line-too-long
        }

        key = self.__format_conversation_history_cache_key(
                game_id=conversation.game_id,
                scene_id=conversation.scene_id,
                session_id=conversation.session_id,
                player_id=conversation.player_id
            )
        history = self._conversation_history.get(key=key)

        if not USE_QUICK_START:
            model = GenerativeModel(
                self._llm_model_name,
                system_instruction=[prompt.prompt_template]
            )
            chat = model.start_chat(history=history)
        else:
            model = quick_start_wrapper(
                model_name=self._llm_model_name,
                system_instruction=prompt.prompt_template,
            )
            logging.info(f"* conversationManager:chat|history : {type(history)} | {history}")

            chat = model.start_chat(history=history)

        result = chat.send_message(
                [conversation.input],
                generation_config=generation_config,
                safety_settings=safety_settings
            )
        logging.info(f"* conversationManager:chat|result : {result}")
        if result is not None:
            self._conversation_history.set(
                key, chat.history
            )
            return result, chat.history
        else:
            return None, chat.history
