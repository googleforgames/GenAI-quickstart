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
Baseball Game Router

Game Logic for Baseball simulation game

Attributes:
    router (object): FastAPI router object for baseball simulation
"""

import os
import json
import tomllib
import logging

from fastapi import (
    APIRouter,
    HTTPException,
    WebSocket,
    WebSocketDisconnect
)
from websockets.exceptions import ConnectionClosed

from typing import Optional, Union
from utils.cacheWrapper import CacheFactory
from utils.baseball import BaseballGameHelper, format_lineup, format_current_state
from models.baseball import (
    TeamData,
    GetTeamsRequest,
    UpdateLineupRequest,
    Lineup,
    UpdateRosterRequest,
    Roster,
    GetSuggestionsResponse,
    GetSuggestionsRequest
)
from models.scence import (
    NPCSceneConversationRequest,
    NPCSceneConversationResponse
)
from routers.scene import chat
from utils.baseball_streaming import chat_streaming

# ----------------------------------------------------------------------------#
# Load configuration file (config.toml) and global configs
TOML_PATH = "config.toml" if os.environ["CONFIG_TOML_PATH"] == "" else os.environ["CONFIG_TOML_PATH"]
with open(TOML_PATH, "rb") as f:
    config = tomllib.load(f)

router = APIRouter(prefix="/game", tags=["Game"])

# ----------------------------------Variables and Functions---------------------------------------#

# ----------------------------------GET---------------------------------------#
@router.get(
    path="/teams/{team_id}"
)
def get_teams(team_id:str | None = None) -> list[TeamData]:
    """
    Get Team data
    Args:
        session_id (str): session id.
        team_id (str): select baseball team id.
                    if none team id is given, returns all teams.
                    if team_id = "all", returns all teams.

    Returns:
        GetTeamsResponse object.
    """
    baseball = BaseballGameHelper(config=config)
    try:
        if team_id == "all" or team_id is None:
            teams = baseball.get_teams()
        else:
            teams = baseball.get_team(team_id=team_id)
            # print(f"===\n{type(teams)}\n{teams}\n===")
        return teams
    except Exception as e:
        raise e
        raise HTTPException(status_code=400,
                    detail=f"Error: {e}") from e

@router.get(
    path="/rosters/{session_id}/{player_id}/{team_id}"
)
def get_rosters(session_id:str, player_id:str, team_id:str) -> Optional[Roster]:
    """
    Get Team roster
    Args:
        session_id (str): session id.
        team_id (str): select baseball team id.
                    if none team id is given, returns all teams.

    Returns:
        Roster object.
    """
    baseball = BaseballGameHelper(config=config)
    try:
        team = baseball.get_roster(team_id=team_id,
                                   session_id=session_id,
                                   player_id=player_id)
        return team
    except Exception as e:
        raise HTTPException(status_code=400,
                    detail=f"Error: {e}") from e


@router.get(
    path="/lineup/{session_id}/{player_id}/{team_id}"
)
def get_lineup(session_id:str, player_id:str, team_id:str) -> Optional[Lineup]:
    """
    Get Team roster
    Args:
        session_id (str): session id.
        team_id (str): select baseball team id.
                    if none team id is given, returns all teams.

    Returns:
        GetTeamsResponse object.
    """
    baseball = BaseballGameHelper(config=config)
    try:
        team = baseball.get_lineup(team_id=team_id,
                                   player_id=player_id,
                                   session_id=session_id)
        return team
    except Exception as e:
        raise HTTPException(status_code=400,
                    detail=f"Error: {e}") from e


# ----------------------------------POST---------------------------------------#
@router.post(
    path="/lineup"
)
def update_lineup(lineup:UpdateLineupRequest) -> None:
    """
    Update team lineup
    Args:
        lineup (UpdateLineupRequest): UpdateLineupRequest object.

    Returns:
        None.
    """
    baseball = BaseballGameHelper(config=config)
    baseball.update_lineup(
        team_id=lineup.team_id,
        session_id=lineup.session_id,
        player_id=lineup.player_id,
        lineup=lineup.lineup
    )

@router.post(
    path="/rosters"
)
def update_roster(roster:UpdateRosterRequest) -> None:
    """
    Update team roster
    Args:
        roster (UpdateRosterRequest): UpdateRosterRequest object.

    Returns:
        None.
    """
    baseball = BaseballGameHelper(config=config)
    baseball.update_roster(
        team_id=roster.team_id,
        session_id=roster.session_id,
        player_id=roster.player_id,
        roster=roster.roster
    )

@router.post(
    path="/get_suggestions"
)
def get_suggestions(req:GetSuggestionsRequest) -> NPCSceneConversationResponse:
    """
    Get Tactics suggestions and recommendations
    Args:
        req (GetSuggestionsRequest): GetSuggestionsRequest object.

    Returns:
        NPCSceneConversationResponse object.
    """
    # return _get_suggestions(req=req, ws=None, func=None)
    baseball = BaseballGameHelper(config=config)
    player_lineup = baseball.get_lineup(
        team_id=req.player_team_id,
        session_id=req.session_id,
        player_id=req.player_id
    )
    computer_lineup = baseball.get_lineup(
        team_id=req.computer_team_id,
        session_id=req.session_id,
        player_id="Computer"
    )
    if player_lineup is not None:
        logging.info(f"** player_lineup:{json.dumps(player_lineup)}")
    else:
        logging.info(f"** player_lineup is None")
    if computer_lineup is not None:
        logging.info(f"** computer_lineup:{json.dumps(computer_lineup)}")
    else:
        logging.info(f"** computer_lineup is None")
    # TODO: format the current state
    final_input = f"""
### Player lineup

{format_lineup(lineup=player_lineup)}

### Opponent lineup

{format_lineup(lineup=computer_lineup)}

### Current State

Player plays the `home` team.

{format_current_state(req.input)}
    """
    conv_req = NPCSceneConversationRequest(
        game_id = config["game"]["game_id"],
        player_id = req.player_id,
        npc_id = "coach",
        input = final_input,
        in_game_time = "",
        scene_id = req.scene_id,
        session_id = req.session_id
    )
    conv_resp = chat(conv_req)
    return conv_resp

######################
# WebSocket Interface
######################
async def _get_suggestions(req:GetSuggestionsRequest,
                    model:str = "gemini-2.0-flash-001",
                    temperature:float = 1,
                    top_p:float = 0.95,
                    max_output_tokens:int = 8192,
                    ws:Optional[WebSocket] = None,
                    func:any=None) -> NPCSceneConversationResponse:
    """
    Get Tactics suggestions and recommendations
    Args:
        req (GetSuggestionsRequest): GetSuggestionsRequest object.

    Returns:
        NPCSceneConversationResponse object.
    """
    baseball = BaseballGameHelper(config=config)
    player_lineup = baseball.get_lineup(
        team_id=req.player_team_id,
        session_id=req.session_id,
        player_id=req.player_id
    )
    computer_lineup = baseball.get_lineup(
        team_id=req.computer_team_id,
        session_id=req.session_id,
        player_id="Computer"
    )
    # TODO: format the current state
    final_input = f"""
### Team {req.player_team_id} lineup

{format_lineup(lineup=player_lineup)}

### Team {req.computer_team_id} lineup

{format_lineup(lineup=computer_lineup)}

### Current State

{format_current_state(req.input)}
    """
    conv_req = NPCSceneConversationRequest(
        game_id = config["game"]["game_id"],
        player_id = req.player_id,
        npc_id = "coach",
        input = final_input,
        in_game_time = "",
        scene_id = req.scene_id,
        session_id = req.session_id
    )

    if ws is None:
        conv_resp = chat(conv_req)
        return conv_resp
    else:
        await chat_streaming(req=conv_req, websocket=ws, func=func,
                            model = model,
                            temperature = temperature,
                            top_p = top_p,
                            max_output_tokens = max_output_tokens,)

async def response_handler(text:str, ws:WebSocket, req:NPCSceneConversationRequest) -> None:
    """
    Response handler for websocket interface.
    """
    resp = {
        "player_id":req.player_id,
        "npc_ids":[],
        "scene_id":req.scene_id,
        "response":text,
        "session_id":req.session_id,
        "in_game_time":req.in_game_time
    }
    await ws.send_text(json.dumps(resp))


@router.websocket("/streaming")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time communication of baseball game suggestions.

    This endpoint allows clients to connect via WebSockets and receive
    real-time updates and suggestions for the baseball game. It handles
    incoming messages, processes them to generate AI-driven suggestions,
    and streams the responses back to the client.

    Args:
        websocket (WebSocket): The WebSocket connection object.

    Raises:
        WebSocketDisconnect: If the client disconnects from the WebSocket.
        ConnectionClosed: If the WebSocket connection is closed unexpectedly.

    Receives:
        JSON data from the client with the following structure:
        {
            "player_team_id": str,  # ID of the player's team.
            "computer_team_id": str,  # ID of the computer's team.
            "session_id": str,  # ID of the game session.
            "player_id": str,  # ID of the player.
            "scene_id": str,  # ID of the current scene.
            "input": str,  # Current game state or player's input.
            "temperature": float, # Temperature for the LLM
        }

    Sends:
        JSON data to the client with the following structure:
        {
            "player_id": str,  # ID of the player.
            "npc_ids": list[str], # List of NPC ids
            "scene_id": str,  # ID of the current scene.
            "response": str,  # AI-generated response or suggestion.
            "session_id": str,  # ID of the game session.
            "in_game_time": str # Current in game time
        }
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            obj = json.loads(data)
            temperature = obj["temperature"] if "temperature" in obj else 0
            print(f"* temperature={temperature}")
            req = GetSuggestionsRequest(
                player_team_id=obj["player_team_id"],
                computer_team_id=obj["computer_team_id"],
                session_id=obj["session_id"],
                player_id=obj["player_id"],
                scene_id=obj["scene_id"],
                input=obj["input"]
            )
            await _get_suggestions(req=req,
                                    ws=websocket,
                                    func=response_handler,
                                    temperature=temperature)
    except (WebSocketDisconnect, ConnectionClosed):
        logging.error("websocket connection closed")

