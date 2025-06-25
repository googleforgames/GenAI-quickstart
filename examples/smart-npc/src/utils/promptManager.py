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

import re
import os
import logging

from models.prompt import PromptRetrievalResponse
from models.npc import (
    NPCInfoResponse,
    NPCInfoRequest
)
from utils.cacheWrapper import CacheFactory
from utils.database import DataConnection
from utils.sceneManager import SceneManager
from utils.npcManager import NPCManager
from utils.conversationManager import ConversationManager

"""
Prompt Management Help class
"""
class PromptManager():
    """
    Helper class for prompt management.
    """
    def __init__(self, config:dict):
        """
        Initialize the prompt manager helper class.

        Args:
            config (dict): config.toml dict.
        """
        self._cache = CacheFactory(config=config).get_cache("prompts")
        self._config = config
        self._connection = DataConnection(config=config)

    def __format_cache_key(self, game_id:str, scene_id:str, prompt_id:str) -> str:
        """
        Format prompt cache key
        """
        return f"{game_id}/{scene_id}/{prompt_id}"

    def __extract_placeholders(self, prompt:str):
        """
        Extracts placeholder names from a prompt string.

        Args:
            prompt (str): The prompt string containing placeholders enclosed in curly braces.

        Returns:
            A list of placeholder names found in the prompt.
        """
        pattern = r"{([^}]+)}"
        matches = re.findall(pattern, prompt)

        # some prompts may use {}, disregard those.
        return [m for m in matches if not any(c in m for c in (" ", "\"", "\n"))]

    def get_prompt_template(
            self,
            prompt_id:str,
            scene_id:str="default"
        ) -> str:
        """
        Get Prompt template.

        Args:
            prompt_id (str): prompt id
            scene_id (str): scene_id, defaults to "default"

        Returns:
            Prompt template.
        """
        game_id = self._config["game"]["game_id"]
        key = self.__format_cache_key(game_id=game_id,
                                      scene_id=scene_id,
                                      prompt_id=prompt_id)
        prompt_template = self._cache.get(key=key)

        if not prompt_template:
            # If prompt template is not cached.
            sql = self._config["sql"]["QUERY_PROMPT_TEMPLATE"]
            results = self._connection.execute(
                sql = sql,
                sql_params={
                    "prompt_id":prompt_id,
                    "scene_id":scene_id,
                    "game_id":game_id
                }
            )
            for prompt in results:
                prompt_template = prompt[3]
                if prompt[0] == scene_id:
                    self._cache.set(key, prompt_template)
                    break
                else:
                    prompt_id = prompt[0]
                    logging.info("* setting cache; %s | %s | %s",
                                game_id,
                                scene_id,
                                prompt_id
                            )
                    self._cache.set(
                        self.__format_cache_key(
                            game_id,
                            scene_id,
                            prompt_id
                        ),
                        prompt_template
                    )
        return prompt_template

    def __construct_prompt(self,
                           prompt_template:str,
                           scene_id:str="default") -> str:
        """
        Replace prompe placeholders with actual prompts

        Args:
            prompt_id (str): prompt id.
            scene_id (str): scene id, defaults to "default"
        Returns:
            Prompt template.
        """
        if prompt_template:
            place_holders = self.__extract_placeholders(prompt_template)
            for place_holder in place_holders:
                place_holder_prompt_template = self.get_prompt_template(
                    prompt_id=place_holder,
                    scene_id=scene_id
                )
                if place_holder_prompt_template:
                    place_holder_prompt_template = self.__construct_prompt(
                                        prompt_template=place_holder_prompt_template,
                                        scene_id=scene_id)
                    prompt_template = prompt_template.replace(
                        "{" + place_holder + "}",
                        place_holder_prompt_template
                    )
        logging.info("Final prompt:\n%s", prompt_template)
        return prompt_template

    def construct_prompt(self, prompt_id:str,
                         scene_id:str="default"
        ) -> PromptRetrievalResponse:
        """
        Get prompt template from the database, parse the template.
        Fill in placeholders with corresponding prompts in the database.
        Returns the conducted prompt.

        Args:
            prompt_id (str): prompt id.
            scene_id (str): scene id, defaults to "default"
        Returns:
            Prompt template.
        """
        logging.info("construct_prompt: %s | %s" ,scene_id, prompt_id)
        prompt_template = self.get_prompt_template(
            prompt_id=prompt_id,
            scene_id=scene_id
        )

        if prompt_template:
            new_prompt_template = self.__construct_prompt(
                prompt_template=prompt_template,
                scene_id=scene_id
            )
            place_holders = self.__extract_placeholders(
                prompt=new_prompt_template
            )
            return self.__update_place_holders(
                prompt_template=PromptRetrievalResponse(
                    game_id=self._config["game"]["game_id"],
                    scene_id=scene_id,
                    prompt_id=prompt_id,
                    prompt_template=new_prompt_template,
                    place_holders=place_holders
                )
            )
        else:
            logging.error(f"construct_prompt():No Prompte Template found:{scene_id} | {prompt_id}")
            raise ValueError("Prompt template not found.")

    def __update_place_holders(self,
                               prompt_template:PromptRetrievalResponse
                            ) -> PromptRetrievalResponse:
        scene_manager = SceneManager(config=self._config)
        scene = scene_manager.get_scence(
            game_id=prompt_template.game_id,
            scene_id=prompt_template.scene_id
        )
        npc_in_the_scene = ",".join([id for id in scene.npc_ids]) if scene.npc_ids is not None else ""
        npc_manager = NPCManager(config=self._config)
        for place_holder in prompt_template.place_holders:
            match place_holder:
                case "NON_PLAYER_CHARACTERS":
                    prompt_template.prompt_template = prompt_template.prompt_template.replace(
                        "{NON_PLAYER_CHARACTERS}",
                        npc_in_the_scene
                    )
                case "SCENE_GOAL":
                    prompt_template.prompt_template = prompt_template.prompt_template.replace(
                        "{SCENE_GOAL}",
                        scene.goal
                    )
                case "CHARACTER_BACKGROUND":
                    npcs = []
                    for npcid in scene.npc_ids if scene.npc_ids is not None else []:
                        npc = npc_manager.get_npc(
                            NPCInfoRequest(
                                npc_id=npcid,
                                game_id=prompt_template.game_id
                            ))
                        if npc is not None:
                            npcs.append(npc)
                    prompt_template.prompt_template = prompt_template.prompt_template.replace(
                        "{CHARACTER_BACKGROUND}",
                        f"{os.linesep}".join([npc.background for npc in npcs]),
                    )
                case "CONVERSATION_EXAMPLE":
                    conv_manager = ConversationManager(config=self._config)
                    example = conv_manager.get_conv_example(
                                    example_id="default"
                                )
                    if example:
                        prompt_template.prompt_template = prompt_template.prompt_template.replace(
                            "{CONVERSATION_EXAMPLE}",
                            example
                        )
                case "CURRENT_SCENE":
                    prompt_template.prompt_template = prompt_template.prompt_template.replace(
                        "{CURRENT_SCENE}",
                        scene.scene
                    )
                case _:
                    if "NPC:" in place_holder:
                        npcid = place_holder.split(":")[-1]
                        npc = npc_manager.get_npc(npc_id=npcid)
                        prompt_template.prompt_template = prompt_template.prompt_template.replace(
                            place_holder,
                            npc.background
                        )
                    else:
                        logging.warning({
                            "message": f"Placeholder: {place_holder} not implemented."
                        })
        return prompt_template