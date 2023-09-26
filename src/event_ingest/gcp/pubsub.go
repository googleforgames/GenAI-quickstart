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

package gcp

import (
    "context"
    "encoding/json"
    "fmt"
    "os"
    
    "cloud.google.com/go/pubsub"
    
    "github.com/gaming-specialists/udp/services/event_ingest/types"
)

func PublishToPubsub(ctx context.Context, payload types.GameEvent) error {

    gcpProjectID := fmt.Sprintf("%v", os.Getenv("GCP_PROJECT_ID"))
    pubsubTopicID := fmt.Sprintf("%v", os.Getenv("PUBSUB_TOPIC_GAME_TELEMETRY"))

    client, err := pubsub.NewClient(ctx, gcpProjectID)

    if err != nil {
        return fmt.Errorf("Failed to initialize PubSub client: %v", err)
    }
    defer client.Close()

    topic := client.Topic(pubsubTopicID)
    defer topic.Stop()

    jsonPayload, err := json.Marshal(payload)
    if err != nil {
        return fmt.Errorf("Failed to marshal JSON payload: %v", err)
    }

    msg := &pubsub.Message{
        Data: jsonPayload,
    }

    // Publish message
    result := topic.Publish(ctx, msg)
    _, err = result.Get(ctx)
    if err != nil {
        return fmt.Errorf("Failed to publish message to PubSub: %v", err)
    }

    return nil
}
