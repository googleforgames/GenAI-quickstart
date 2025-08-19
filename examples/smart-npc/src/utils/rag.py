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

"""RAG helper module
"""
from utils.cacheWrapper import CacheFactory
from utils.llm import text_embedding
from utils.database import DataConnection
from utils.cacheWrapper import CacheWrapper


class RAG:
    """
    Wrapper class for querying Vector Store
    """

    def __init__(self, config:dict):
        """Initialize the RAG object

        Args:
            config (dict): Configuration object.
        """
        # self.__knowledge_cache = CacheFactory(config).get_cache("knowledge")
        self.__quests_cache = CacheFactory(config).get_cache("quests")
        self.config = config

    def __get_query_embedding(self, query:str) -> list[float]:
        """Get Text embeddings of the input query
        Args:
            query (str): input query

        Returns:
            Embeddings
        """
        embeddings = text_embedding(
                        task_type="RETRIEVAL_QUERY",
                        text=query
                    )
        return embeddings

    def __search_relevant_knowledge(
            self,
            sql:str,
            lore_level:int,
            query_embeddings:list[float]) -> list[dict]:
        """Search knowledge relevant to user's query
        Args:
            sql (str): SQL query
            lore_level (int): Min. lore level required
            query_embeddings (list[float]): query's embeddings

        Returns:
            Embeddings
        """
        db = DataConnection(config=self.config)
        rows = db.execute(sql=sql,
                sql_params={"query_embeddings": f"{query_embeddings}",
                "lore_level":lore_level})
        resutls = []
        print(f"* __search_relevant_knowledge={rows}")
        for row in rows:
            resutls.append({
                "background_name": row[0],
                "content": row[1],
                "lore_level": row[3],
                "background": row[4],
                "score": row[5]
            })

        return resutls

    def search_knowledge(self, query:str, lore_level:int) -> list[dict]:
        """Search knowledge relevant to user's query
        Args:
            sql (str): SQL query
            lore_level (int): Min. lore level required
            query_embeddings (list[float]): query's embeddings

        Returns:
            Relevant knowledge
        """
        query_embeddings = self.__get_query_embedding(query=query)
        print(self.config["sql"]["QUERY_NPC_KNOWLEDGE"])
        knowledge = self.__search_relevant_knowledge(
            sql=self.config["sql"]["QUERY_NPC_KNOWLEDGE"],
            lore_level=lore_level,
            query_embeddings=query_embeddings
        )

        return knowledge

    def __search_quests(self, sql:str, provider_id:str) -> list[dict]:
        """Search quests provided by the NPC
        Args:
            sql (str): SQL query
            provider_id (str): NPC's unique id

        Returns:
            Quests can be provided by this NPC
        """
        resp = self.__quests_cache.get(provider_id)
        if resp is not None:
            return resp
        else:
            db = DataConnection(config=self.config)
            rows = db.execute(sql=sql, sql_params={"provider_id": provider_id})

            resutls = []
            for row in rows:
                print(f"** row={row}")
                resutls.append({
                    "quest_id": row[0],
                    "quest_story": row[1],
                    "min_level": int(row[2]),
                    "metadata": row[3],
                    "quest_name": row[4],
                    "provider_id": row[5]
                })

                self.__quests_cache.set(provider_id, resutls)
            return resutls

    def search_quests(self, provider_id:str) -> list[dict]:
        """Search quests provided by the NPC
        Args:
            provider_id (str): NPC's unique id

        Returns:
            Quests can be provided by this NPC
        """
        # Instead of query relevant quests,
        # fetch all quests that can be provided by this NPC
        quests = self.__search_quests(
            sql=self.config["sql"]["QUERY_SEARCH_QUESTS_ALL"],
            provider_id=provider_id
        )

        return quests
