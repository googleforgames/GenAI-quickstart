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
Prompt Management Router

Entry points of Prompt Management related actions.

Attributes:
    router (object): FastAPI router object for Prompt Management
"""

import os
import tomllib

from fastapi import APIRouter, HTTPException

from utils.promptManager import PromptManager
from models.prompt import PromptRetrievalRequest, PromptRetrievalResponse

router = APIRouter(prefix="/prompts", tags=["Prompt Management"])

# ----------------------------------------------------------------------------#
# Load configuration file (config.toml) and global configs
TOML_PATH = "config.toml" if os.environ["CONFIG_TOML_PATH"] == "" else os.environ["CONFIG_TOML_PATH"]
with open(TOML_PATH, "rb") as f:
    config = tomllib.load(f)

# ----------------------------------GET---------------------------------------#
@router.get(
    path="/{game_id}/{scene_id}/{prompt_id}"
)
def get_prompt(
        game_id:str, scene_id:str, prompt_id:str
    ) -> PromptRetrievalResponse:
    """
    Get prompt template by id.
    Args:
        game_id (str): game id.
        scene_id (str): scene id.
    Returns:
        PromptRetrievalResponse object.
    Raises:
        ValueError: If the game id is invalid.
    """
    try:
        if game_id != config["game"]["game_id"]:
            raise ValueError("Invalid game id.")

        prompt_tempalte = PromptManager(config=config).construct_prompt(
            prompt_id=prompt_id,
            scene_id=scene_id
        )
        return prompt_tempalte
    except Exception as e:
        raise HTTPException(status_code=400,
                    detail=f"Error: {e}") from e
