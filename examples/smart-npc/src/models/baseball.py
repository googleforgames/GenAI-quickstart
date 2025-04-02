"""
FastAPI Baseball Game Request / Response Models
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

from typing import Optional, Union
from pydantic import BaseModel

class GetTeamsRequest(BaseModel):
    """
    GetTeamsRequest is used to get a list of teams.
    """
    team_id: Optional[str]

class TeamData(BaseModel):
    """
    TeamData is used to store team data.
    """
    team_id: str
    team_name: str
    description: str
    roster: dict
    team_year: int
    default_lineup: dict

class GetTeamsResponse(BaseModel):
    """
    GetTeamsResponse is used to return a list of teams.
    """
    teams: list[TeamData]

class UpdateRosterRequest(BaseModel):
    """
    UpdateRosterRequest is used to update a roster.
    """
    team_id: str
    player_id: str
    roster: dict
    session_id: str

class Roster(BaseModel):
    """
    Roster is used to store a roster.
    """
    team_id: str
    player_id: str
    roster: dict
    session_id: str

class UpdateLineupRequest(BaseModel):
    """
    UpdateLineupRequest is used to update a lineup.
    """
    team_id: str
    player_id: str
    lineup: dict
    session_id: str

class Lineup(BaseModel):
    """
    Lineup is used to store a lineup.
    """
    team_id: str
    player_id: str
    lineup: dict
    session_id: str

class GetSuggestionsRequest(BaseModel):
    """
    GetSuggestionsRequest is used to get suggestions.
    """
    player_team_id: str
    computer_team_id: str
    session_id: str
    player_id: str
    scene_id: str
    input: str = ""

class GetSuggestionsResponse(BaseModel):
    """
    GetSuggestionsResponse is used to return suggestions.
    """
    player_id: str
    response: Union[str, dict]
    session_id: str
