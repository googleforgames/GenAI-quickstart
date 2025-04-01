"""
Knowledge Retrival Router

Retrive relevant documents.

Attributes:
    router (object): FastAPI router object for Knowledge retrival
"""

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

import os
import tomllib
import vertexai.preview.generative_models as generative_models

from fastapi import APIRouter

from utils.rag import RAG

from models.npc import (
    SearchNPCKnowledgeRequest,
    Knowledge,
    SearchNPCKnowledgeResponse
)

# ----------------------------------------------------------------------------#
# Load configuration file (config.toml) and global configs
TOML_PATH = "config.toml" if os.environ["CONFIG_TOML_PATH"] == "" else os.environ["CONFIG_TOML_PATH"]
with open(TOML_PATH, "rb") as f:
    config = tomllib.load(f)

# ----------------------------------------------------------------------------#

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH, # pylint: disable=line-too-long
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,   # pylint: disable=line-too-long
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,   # pylint: disable=line-too-long
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,  # pylint: disable=line-too-long
}
# ----------------------------------------------------------------------------#

router = APIRouter(prefix="/knowledge", tags=["NPC - Knowledge"])


@router.post(
    path="/search_knowledge"
)
def search_knowledge(
        req:SearchNPCKnowledgeRequest
    ) -> SearchNPCKnowledgeResponse:
    """Search knowledge relevant to user's input query

    Args:
        req: Player's input query.

    Returns:
        Knowledge that is relevant to the query.
    """
    rag = RAG(config=config)
    results = rag.search_knowledge(
        query=req.query,
        lore_level=req.npc_lore_level
    )
    information = []
    for result in results:
        information.append(
            Knowledge(
                knowledge = result["background"],
                lore_level = int(result["lore_level"]),
                score = float(result["score"])
            )
        )
    return SearchNPCKnowledgeResponse(
        knowledge=information
    )
