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

# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/memorystore/redis/main.py
# https://redis.io/learn/develop/python/fastapi
"""Cache Wrapper

Wrapper of cache mechanism.
This implementation uses in-memory cache.

Attributes:
    router (object): FastAPI router object for cache wrapper

TODO:
    Migrate to Redis cache
"""

import os
import redis

from pickle import loads, dumps
from typing import Union

class RedisCacheWrapper:
    """
    Wraps the cache mechanism.

    Note:
        This implementation uses in-memory cache.
    """
    def __init__(self, config, prefix):
        """
        Initialize the CacheWrapper object
        """
        self.__key_prefix = prefix
        self.__config = config
        redis_host = self.__config["gcp"]["cache-server-host"]
        redis_port = int(self.__config["gcp"]["cache-server-port"])
        self.__client = redis.StrictRedis(host=redis_host, port=redis_port)

    def __key(self, key:str) -> str:
        return f"{self.__key_prefix}/{key}"

    def get(self, key:str) -> any:
        """Get cached item by key.

        Args:
            key: Key of the cached item.

        Returns:
            Cached item.
        """
        if self.__client.get(dumps(self.__key(key))) is not None:
            return loads(self.__client.get(dumps(self.__key(key))))
        else:
            return None

    def keys(self) -> list[str]:
        """Get keys.

        Returns:
            Cached keys.
        """
        results = []
        for key in self.__client.keys():
            results.append(
                f"""{loads(key)}:{loads(self.__client.get(loads(key))) if self.__client.get(loads(key)) is not None else ""}"""
            )
        return results
        # return [f"{loads(key)}:{loads(self.__client.get(loads(key)))}" for key in self.__client.keys()]
        # return [loads(key) for key in self.__client.keys() if loads(key).startswith(self.__key_prefix + "_")]

    def set(self, key:str, value:any) -> None:
        """Add item to the cache.

        Args:
            key: Key of the cached item.
            value: Item to be cached
        """
        self.__client.set(name=dumps(self.__key(key)), value=dumps(value))

    def delete(self, key:str) -> None:
        """Delete an item from the cache.

        Args:
            key: Key of the cached item.
        """
        self.set(key, None)
        self.__client.delete(dumps(self.__key(key)))
        self.__client.delete(dumps(key))


class CacheWrapper:
    """
    Wraps the cache mechanism.

    Note:
        This implementation uses in-memory cache.
    """
    def __key(self, key:str) -> str:
        return f"{self.__key_prefix}/{key}"

    def __init__(self, config, prefix):
        """
        Initialize the CacheWrapper object
        """
        self.__key_prefix = prefix
        self.__cache = {}

    def get(self, key:str) -> any:
        """Get cached item by key.

        Args:
            key: Key of the cached item.

        Returns:
            Cached item.
        """
        print(f"* getting key={key}")
        print(f"self.__key(key)={self.__key(key)}")

        if self.__key(key) in self.__cache.keys():
            return self.__cache[self.__key(key)]
        else:
            print(f"* no {key}:{self.__key(key)}")
            return None

    def keys(self) -> any:
        """Get keys.

        Returns:
            Cached keys.
        """
        results = []
        for key in self.__cache.keys():
            results.append(f"[{key}]:{self.__cache[key]}")
        # return self.__cache.keys()
        return results

    def set(self, key:str, value:any) -> None:
        """Add item to the cache.

        Args:
            key: Key of the cached item.
            value: Item to be cached
        """
        self.__cache[self.__key(key)] = value

    def delete(self, key:str) -> None:
        """Delete an item from the cache.

        Args:
            key: Key of the cached item.
        """
        self.__cache.pop(self.__key(key), None)

in_memory_cache = {}

class CacheFactory:
    def __init__(self, config):
        self.__config = config

    def get_cache(self, key_prefix:str) -> Union[CacheWrapper, RedisCacheWrapper]:
        if self.__config["gcp"]["use-cache-server"] == "True":
            return RedisCacheWrapper(self.__config, key_prefix)
        else:
            global in_memory_cache
            if key_prefix in in_memory_cache.keys():
                return in_memory_cache[key_prefix]
            else:
                cache = CacheWrapper(self.__config, key_prefix)
                in_memory_cache[key_prefix] = cache
                return cache
