# Copyright 2024 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fastapi import FastAPI
from pydantic import BaseModel

import logging
import npc
import requests
import sys
import traceback

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)

app = FastAPI(
    redoc_url=None,
    title="API for Vertex AI Chat LLM",
    description="Contains business logic, data processing steps, and uses the GCP SDK to call the Google Cloud Vertex chat-bison LLM model.",
    version="0.0.1",
)


def get_gcp_metadata():
    metadata_server = "http://metadata.google.internal"
    headers = {"Metadata-Flavor": "Google"}

    # Get Project ID
    project_id_url = f"{metadata_server}/computeMetadata/v1/project/project-id"
    project_id_response = requests.get(project_id_url, headers=headers)
    project_id = project_id_response.text if project_id_response.status_code == 200 else "Unavailable"

    # Get GCP Zone
    zone_url = f"{metadata_server}/computeMetadata/v1/instance/zone"
    zone_response = requests.get(zone_url, headers=headers)
    zone = zone_response.text.split('/')[-1] if zone_response.status_code == 200 else "Unavailable"

    # Extract GCP Region
    region = '-'.join(zone.split('-')[:-1])

    return project_id, region


def get_config():
    project, region = get_gcp_metadata()
    cfg = npc.data_from_file(npc.CONFIG_PATH)
    cfg['global']['project'] = project
    cfg['global']['location'] = "us-central1" # TODO: us-central1 allows batches of 250, other regions only 5?
    return cfg


cfg = get_config()
genai = npc.genai_from_config(cfg)
db = npc.db_from_config(cfg, genai)
world_data = npc.data_from_file(npc.WORLD_PATH)
npcs = npc.npcs_from_world(world_data, genai, db)


class Payload_NPC_Chat(BaseModel):
    message: str
    from_id: int
    to_id: int
    debug: bool | None = False


# Routes


@app.post("/")
def npc_chat(payload: Payload_NPC_Chat):
    try:
        resp = npcs[0].reply(payload.from_id, "Jane", payload.message)
        if not payload.debug:
            # Filter to just the response
            resp = {"response": resp['response']}
        return resp
    except Exception as e:
        raise


@app.get("/genai_health", include_in_schema=False)
async def health_check():
    return {'status': 'ok'}


@app.post("/reset_world_data")
def reset_world_data():
    try:
        db.reinitialize(world_data)
        return {'status': 'ok'}
    except Exception as e:
        traceback.print_exc()
        raise


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7777)