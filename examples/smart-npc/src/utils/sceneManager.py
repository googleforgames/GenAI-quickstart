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

from models.scence import Scene
from utils.cacheWrapper import CacheFactory
from utils.database import DataConnection

"""
Scene Management Help class
"""
class SceneManager():
    """
    Helper class for scene management.
    """
    def __init__(self, config:dict):
        """
        Initialize the scene manager helper class.

        Args:
            config (dict): config.toml dict.
        """
        self._cache = CacheFactory(config=config).get_cache("scenes")
        self._config = config
        self._connection = DataConnection(config=config)

    def __format_cache_key(self, game_id:str, scene_id:str) -> str:
        """
        Format prompt cache key
        """
        return f"{game_id}/{scene_id}"

    def get_scence(self,
                   game_id:str,
                   scene_id:str) -> Scene:
        """
        Get Scene configuration.
        Args:
            game_id (str): game id.
            scene_id (str): scene id.

        Returns:
            Scene configuraiton object.
        """
        if game_id != self._config["game"]["game_id"]:
            raise ValueError("Invalid game id.")
        key = self.__format_cache_key(
            game_id=game_id,
            scene_id=scene_id
        )
        scene = self._cache.get(key)

        if scene is not None:
            return scene
        try:
            connection = DataConnection(config=self._config)

            sql = self._config["sql"]["QUERY_SCENE"]
            rows = connection.execute(sql, {
                "scene_id": scene_id,
                "game_id": self._config["game"]["game_id"]
            })
            for row in rows:
                resp = Scene(
                    game_id=row[6],
                    scene_id=row[0],
                    scene=row[1],
                    goal=row[3],
                    npc_ids=[n.strip() for n in f"{row[4]}".split(",")],
                    status=row[2],
                    knowledge=row[5]
                )
                self._cache.set(key, resp)
                return resp
        except Exception as e:
            raise e
