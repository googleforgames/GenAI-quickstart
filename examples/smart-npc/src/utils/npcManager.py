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

from models.npc import NPCInfoRequest, NPCInfoResponse
from models.prompt import PromptRetrievalResponse
from utils.cacheWrapper import CacheFactory
from utils.database import DataConnection
from utils.sceneManager import SceneManager

"""
NPC Management Help class
"""
class NPCManager():
    """
    Helper class for npc management.
    """
    def __init__(self, config:dict):
        """
        Initialize the prompt manager helper class.

        Args:
            config (dict): config.toml dict.
        """
        self._cache = CacheFactory(config=config).get_cache("npcs")
        self._config = config
        self._connection = DataConnection(config=config)

    def __format_cache_key(self, game_id:str, npc_id:str) -> str:
        """
        Format prompt cache key
        """
        return f"{game_id}/{npc_id}"

    def get_npc(self, npc:NPCInfoRequest) -> NPCInfoResponse:
        """Get NPC configuration by id

        Args:
            npc_id: unique id of the NPC.

        Returns:
            NPC information object.
        """
        key = self.__format_cache_key(
            game_id=npc.game_id,
            npc_id=npc.npc_id
        )
        resp = self._cache.get(key)
        if resp is not None:
            return resp
        try:
            sql = self._config["sql"]["QUERY_NPC_BY_ID"]
            npc = self._connection.execute(sql,
                    {
                        "npc_id": npc.npc_id,
                        "game_id": npc.game_id
                    })
            for row in npc:
                resp = NPCInfoResponse(
                    game_id = row[1],
                    background = row[2],
                    name = row[3],
                    npc_class = row[4],
                    class_level = row[5],
                    npc_id = row[0],
                    status = row[6],
                    lore_level = int(row[7])
                )
                self._cache.set(key, resp)
                return resp
            return None
        except Exception as e:
            raise e
