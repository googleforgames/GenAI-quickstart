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

package main

import (
    "encoding/json"
    "fmt"
    "net"
    "log"
    "os"
    "context"
    
    "github.com/gaming-specialists/udp/services/event_ingest/types"
    "github.com/gaming-specialists/udp/services/event_ingest/gcp"
    ml "github.com/gaming-specialists/udp/services/event_ingest/ml"
)

const (
    tcpPort = "7777"
)

func handleConnection(conn net.Conn, ctx context.Context) {

    defer conn.Close()

    
    var ge types.GameEvent
    decoder := json.NewDecoder(conn)
    if err := decoder.Decode(&ge); err != nil {
        log.Println("Error decoding JSON:", err)
        return
    }

    // if payload is tagged for scoring (via "ml" key), then
    // send to the ml endpoint for scoring.
    mlEndpointURI := ctx.Value("mlEndpointURI").(string)
    if (ge.ML != "") && (mlEndpointURI != "") {
        fmt.Println("Sending data to ML Endpoint")
        score, err := ml.ScoreEvent(ctx, ge)
        if err != nil {
            fmt.Println("Error sending data to ML Endpoint via REST")
        } else {
            fmt.Println("Score: ", score)

            // convert the prediction struct to a json payload
            scoreEventJSON, err := json.Marshal(score)
            if err != nil {
                fmt.Println("Error handling ML score", err.Error())
            }

            // respond with scored json payload
            _, err = conn.Write(scoreEventJSON)
            if err != nil {
                fmt.Println("Error returning ML score", err.Error())
            }
        }
    }

    // send to pubsub
    fmt.Println("Sending data to Google PubSub")
    if err := gcp.PublishToPubsub(ctx, ge); err != nil {
        fmt.Println("Error publishing message to Pubsub:", err)
    } else {
        fmt.Println("Successfully sent payload to Pubsub.")
    }

}

func main() {

    // invoke listener
    ln, err := net.Listen("tcp", fmt.Sprintf(":%v", tcpPort))
    if err != nil {
        fmt.Println("Error creating TCP listener:", err)
        return
    }
    defer ln.Close()

    fmt.Println("TCP server started on port:", tcpPort)

    // set ml endpoint uri
    mlAgentEndpoint := os.Getenv("ML_AGENT_URL")
    var mlEndpointURI string
    if mlAgentEndpoint != "" {
        mlEndpointURI = fmt.Sprintf("http://%v/v1/models/mlmodel_v1:predict", mlAgentEndpoint)
        fmt.Println("Using ML Endpoint:", mlEndpointURI)
    } else {
        fmt.Println("ML Endpoint is empty. No ML scoring available to event ingest service.")
        mlEndpointURI = ""
    }

    // attach values to context
    ctx := context.WithValue(context.Background(), "mlEndpointURI", mlEndpointURI)      

    for {
        conn, err := ln.Accept()
        if err != nil {
            fmt.Println("Error accepting connection:", err)
            continue
        } else {
            fmt.Println("Accepted connection")
        }

        // process received data
        go handleConnection(conn, ctx)
    }
}
