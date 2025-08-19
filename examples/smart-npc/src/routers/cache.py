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
Cache Router

Managing Cache

Attributes:
    router (object): FastAPI router object for Cache operations
"""

import os
import json
import tomllib

from fastapi import APIRouter
from typing import Optional, Union
from utils.cacheWrapper import CacheFactory, CacheWrapper, RedisCacheWrapper

# ----------------------------------------------------------------------------#
# Load configuration file (config.toml) and global configs
TOML_PATH = "config.toml" if os.environ["CONFIG_TOML_PATH"] == "" else os.environ["CONFIG_TOML_PATH"]
with open(TOML_PATH, "rb") as f:
    config = tomllib.load(f)


# ----------------------------------------------------------------------------#

router = APIRouter(prefix="/cache", tags=["Cache"])

__AVAILABLE_CACHES = ["npcs", "conversations", "scenes", "conversation_history", "game"]

def __get_cache_server(cache_key:str) -> Optional[Union[CacheWrapper, RedisCacheWrapper]]:
    if cache_key in __AVAILABLE_CACHES:
        return CacheFactory(config).get_cache(cache_key)
    else:
        return None


# ----------------------------------GET---------------------------------------#
@router.get(
    path="/keys"
)
def keys(cache_key:str) -> Optional[list[str]]:
    """
    List cached item keys

    Parmas:
        cache_key: one of ["npc", "quests", "conversations", "scene"]

    Returns:
        List of cached keys
    """
    cacheServer = __get_cache_server(cache_key=cache_key)
    if cacheServer is None:
        return None
    # keys = [key for key in cacheServer.keys() if cacheServer.get(key[key.index("_") + 1:]) is not None]
    return cacheServer.keys()

@router.get(
    path="/{cache_key}/items/{key}"
)
def get_item(cache_key:str, key:str) -> str:
    """
    List cached item keys

    Returns:
        List of cached keys
    """
    cacheServer = __get_cache_server(cache_key=cache_key)
    return f"{cacheServer.get(key=key)}"

# ----------------------------------POST---------------------------------------#
@router.post(
    path="/{cache_key}/{key}"
)
def set_item(cache_key:str, key:str, value:str) -> str:
    """
    Add a string to the cache

    Returns:
        The string
    """
    cacheServer = __get_cache_server(cache_key=cache_key)
    cacheServer.set(key=key, value=value)

    return value

# ----------------------------------DELETE---------------------------------------#
@router.post(
    path="/delete-all"
)
def delete_all() -> str:
    log = ""
    for cache_key in __AVAILABLE_CACHES:
        cache = CacheFactory(config).get_cache(cache_key)
        key_values = cache.keys()
        for kv in key_values:
            key = kv.split(":")[0].replace("[", "").replace("]", "")
            cache.delete(key=key)
            log = log + os.linesep + f"Deleted {key}"
    return log

@router.delete(
    path="/{cache_key}/items/{key}"
)
def delete_item(cache_key:str, key:str) -> list[str]:
    """
    Delete a cached item

    Params:
        key(str): key of the cached item. Use "*" for deleting all cached items.

    Returns:
        None
    """
    keys_deleted = []
    keys_deleted.append(key)
    if key == "*":
        for k in keys(cache_key):
            delete_item(cache_key=cache_key, key=k)
            keys_deleted.append(k)
    else:
        cacheServer = __get_cache_server(cache_key)
        cacheServer.delete(key)
        keys_deleted.append(key)

    return keys_deleted
