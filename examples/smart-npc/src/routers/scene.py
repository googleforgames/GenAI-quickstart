# Copyrightll 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Scene Router

Entry points of Scene related actions.

Attributes:
    router (object): FastAPI router object for Scene actions
"""

import os
import tomllib
import logging
import json

from fastapi import APIRouter, HTTPException

from utils.cacheWrapper import CacheFactory
from utils.llmValidator import LLMValidator
from utils.conversationManager import ConversationManager
from models.scence import (
    NPCSceneConversationRequest,
    NPCSceneConversationResponse,
    Scene
)

from utils.sceneManager import SceneManager
from utils.promptManager import PromptManager
from utils.conversationManager import ConversationManager

router = APIRouter(prefix="/scenes", tags=["SCENCE - Conversations"])

# ----------------------------------------------------------------------------#
# Load configuration file (config.toml) and global configs
TOML_PATH = "config.toml" if os.environ["CONFIG_TOML_PATH"] == "" else os.environ["CONFIG_TOML_PATH"]
with open(TOML_PATH, "rb") as f:
    config = tomllib.load(f)

# ----------------------------------Variables and Functions---------------------------------------#
cached_conv_example = CacheFactory(config).get_cache("conv_example")

def substring_occurence(test_str:str, test_sub:str) -> int:
    """
    Count the number of occurences of a substring in a string.
    Args:
        test_str (str): The string to search in.
        test_sub (str): The substring to search for
    Returns:
        int: The number of occurences of the substring in the string.
    """
    occurence = len(test_str.split(test_sub)) - 1

    return occurence

def ensure_json_dict(input:any) -> dict:
    """
    Ensure that the input is a valid JSON dictionary.
    Args:
        input (any): The input to be converted to a JSON dictionary.
    Returns:
        dict: The input converted to a JSON dictionary.
    """
    if isinstance(input, dict):
        return input
    elif isinstance(input, str):
        try:
            return ensure_json_dict(json.loads(input))
        except json.JSONDecodeError as e:
            logging.error(f"* Unable to decode json string:{e}")
            return {}
# ----------------------------------GET---------------------------------------#
@router.get(
    path="/{scene_id}"
)
def get_scence(game_id:str, scene_id:str) -> Scene:
    """
    Get Scene configuration.
    Args:
        game_id (str): game id.
        scene_id (str): scene id.

    Returns:
        Scene configuraiton object.
    """
    if game_id != config["game"]["game_id"]:
        raise ValueError("Invalid game id.")
    try:
        scene = SceneManager(config=config).get_scence(
            game_id=game_id,
            scene_id=scene_id
        )
        return scene
    except Exception as e:
        raise HTTPException(status_code=400,
                    detail=f"Error: {e}") from e

# ----------------------------------POST---------------------------------------#
@router.post(
    path="/chat"
)
def chat(req:NPCSceneConversationRequest) -> NPCSceneConversationResponse:
    """Generates NPC responses

    Args:
        req: Player's input query.

    Returns:
        NPC's response to the player's inpput.
    """
    if req.game_id != config["game"]["game_id"]:
        raise ValueError("Invalid game id.")

    scene = None
    if req.scene_id:
        logging.info({"message":f"* get_scene: {req.scene_id} | {req.game_id}"})
        scene = get_scence(scene_id=req.scene_id,
                           game_id=req.game_id)

    if scene is None:
        raise HTTPException(status_code=400,
                            detail=f"Scene not found:{req.scene_id}")

    # TODO: No Knowledge at the moment
    # max_lore_level = max([npc.lore_level for npc in npcs])
    # knowledge = search_knowledge(SearchNPCKnowledgeRequest(
    #     npc_lore_level = max_lore_level,
    #     query = req.input
    # ))

    # TODO: Let's revist how to fetch quests in this scene
    # quests = search_quest(
    #     npc_id=req.npc_id
    # )

    # language_code = config["npc"]["RESPONSE_LANGUAGE"]

    # TODO: In this case, we do not need the player information.
    #       Because all charachter information, including the main character inforamtion
    #       is listed with other characters in the prompt.
    # player = get_player_info()

    if scene.goal != "" and scene.goal != "NA":
        prompt_template_id = "NPC_CONVERSATION_SCENCE_GOAL_TEMPLATE"
    else:
        prompt_template_id = "NPC_CONVERSATION_SCENCE_NO_GOAL_TEMPLATE"

    prompt_manager = PromptManager(config=config)
    prompt_template = prompt_manager.construct_prompt(
        prompt_id=prompt_template_id,
        scene_id=req.scene_id
    )
    logging.info(f"""Final Input:

{req.input}
""")
    answer, history = ConversationManager(config=config).chat(
        conversation=req,
        prompt=prompt_template
    )
    logging.info({"message":f"* answer.candidates={answer.candidates}"})
    if answer is not None:
        json_answer_text = answer.candidates[0].content.parts[0].text.replace("```json", "").replace("```", "") # pylint: disable=line-too-long

        logging.info({"message":f"* scene.chat | json_answer_text={json_answer_text}"})
        if config["game"]["enable_validator"] == "True":
            validator = LLMValidator(config=config)
            json_answer_text = validator.validate(
                scene_id=req.scene_id,
                player_input=req.input,
                npc_response=json_answer_text,
                npcs=",".join([id for id in scene.npc_ids]),
                conversation_history=history
            )
        occurence = substring_occurence(test_str=json_answer_text, test_sub="[CHAR(")

        if occurence > 1:
            json_answer_text = json_answer_text.replace("[CHAR(", os.linesep + "[CHAR(")

        json_answer_text = json_answer_text.replace("\\n", "")
        response_text = json_answer_text # f"{ensure_json_dict(json_answer_text)}" # json.loads(json.loads(json_answer_text))

        return NPCSceneConversationResponse(
            player_id=req.player_id,
            npc_id=",".join(scene.npc_ids),
            scene_id=req.scene_id,
            response=response_text, # json_answer_text,
            session_id=req.session_id,
            in_game_time=req.in_game_time
        )
    else:
        logging.error({"message":f"No llm response."})
        raise HTTPException(status_code=400,
                    detail=f"Error: no llm response")
