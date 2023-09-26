// Copyright 2023 Google LLC All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package types

type GameEvent struct {
    EventID       string   `json:"eventid"`
    EventType     string   `json:"eventtype"`
    Timestamp     int64    `json:"timestamp"`
    PlayerID      string   `json:"playerid"`
    Label         string   `json:"label"`
    Xcoord        float64  `json:"xcoord"`
    Ycoord        float64  `json:"ycoord"`
    Zcoord        float64  `json:"zcoord"`
    Dow           int64    `json:"dow"`
    Hour          int64    `json:"hour"`
    Score         int64    `json:"score"`
    MinutesPlayed int64    `json:"minutesplayed"`
    TimeInStore   int64    `json:"timeinstore"`
    ML            string   `json:"ml"`
}

type Prediction struct {
    Predictions  [][]float64 `json:"predictions"`
}
