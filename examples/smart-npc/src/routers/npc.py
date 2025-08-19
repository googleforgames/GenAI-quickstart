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
NPC Router

Entry points of NPC related actions.

Attributes:
    router (object): FastAPI router object for NPC actions
"""

import os
import json
import tomllib

from typing import Optional
from fastapi import APIRouter, HTTPException

from utils.npcManager import NPCManager
from models.npc import (
    NPCInfoRequest,
    NPCInfoResponse
)
from utils.database import DataConnection


# ----------------------------------------------------------------------------#
# Load configuration file (config.toml) and global configs
TOML_PATH = "config.toml" if os.environ["CONFIG_TOML_PATH"] == "" else os.environ["CONFIG_TOML_PATH"]
with open(TOML_PATH, "rb") as f:
    config = tomllib.load(f)

# ----------------------------------------------------------------------------#

router = APIRouter(prefix="/npcs", tags=["NPC - Conversations"])

# ----------------------------------GET---------------------------------------#
@router.get(
    path="/{game_id}/{npc_id}", response_model=NPCInfoResponse
)
def get_npc(npc_id:str, game_id:str) -> NPCInfoResponse:
    """Get NPC configuration by id

    Args:
        npc_id: unique id of the NPC.

    Returns:
        NPC information object.
    """
    manager = NPCManager(config=config)
    npc = manager.get_npc(
                npc=NPCInfoRequest(
                        npc_id=npc_id,
                        game_id=game_id
                    ))
    return npc
