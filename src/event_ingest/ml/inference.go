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

package inference

import (
    "context"
    "encoding/json"
    "fmt"

    "github.com/gaming-specialists/udp/services/event_ingest/types"
    external "github.com/gaming-specialists/udp/services/event_ingest/external"
)

// Defines a function that validates and filters a game event payload,
// then sends the data to an ML endpoint.
func ScoreEvent(ctx context.Context, payload types.GameEvent) (types.Prediction, error) {
    
    // Get ml endpoint URI
    mlEndpointURI := ctx.Value("mlEndpointURI").(string)
    
    // Validate and filter the game event payload to match 
    // the data input structure required by your ML model
    // Convert each value in the map to a float64 and append to the result slice
    data := []float64{
        float64(payload.Xcoord), 
        float64(payload.Ycoord), 
        float64(payload.Zcoord), 
        float64(payload.Dow), 
        float64(payload.Hour), 
        float64(payload.Score), 
        float64(payload.MinutesPlayed),
        float64(payload.TimeInStore),
    }
    
    fmt.Printf("[ Debug ] Data payload received: %v\n", data)

    // "instances" is the key required for our input payload to the Vertex ML model
    instances := [][]float64{data}
    type InputData struct {
        Instances [][]float64 `json:"instances"`
    }

    inputData := InputData{Instances: instances}

    // Convert the struct to JSON
    jsonData, err := json.Marshal(inputData)
    if err != nil {
        fmt.Println("Error with json marshal in ScoreEvent")
        return types.Prediction{}, err
    }

    // Send data to our ML service for scoring
    resp, err := external.PostJSON(mlEndpointURI, jsonData)
    if err != nil {
        fmt.Println("Error posting to REST URI in ScoreEvent")
        return types.Prediction{}, err
    }

    var prediction types.Prediction
    err = json.NewDecoder(resp.Body).Decode(&prediction)
    if err != nil {
        fmt.Println("Error decoding json in ScoreEvent")
        return types.Prediction{}, err
    }

    return prediction, err
}
