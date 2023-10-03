# Copyright 2023 Google LLC All Rights Reserved.
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
FROM golang:1.20.3 as builder

# Create and change to the app directory.
WORKDIR /app

# Retrieve application dependencies.
# Expecting to copy go.mod and if present go.sum.
COPY go.* ./
COPY main.go ./
COPY ./external ./external
COPY ./gcp ./gcp
COPY ./ml ./ml
COPY ./types ./types

RUN go mod download

# Build the binary.
RUN go build -v -o server

# Use the official Debian slim image for a lean production container.
# https://hub.docker.com/_/debian
# https://docs.docker.com/develop/develop-images/multistage-build/#use-multi-stage-builds
FROM debian:buster-slim
RUN set -x && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy the binary to the production image from the builder stage.
COPY --from=builder /app/server /app/server

# Set ENV variables that persist at runtime

ARG PUBSUB_TOPIC_GAME_TELEMETRY
ENV PUBSUB_TOPIC_GAME_TELEMETRY="$PUBSUB_TOPIC_GAME_TELEMETRY"

ARG GCP_PROJECT_ID
ENV GCP_PROJECT_ID="$GCP_PROJECT_ID"

EXPOSE 7777

# Run the web service on container startup.
CMD ["/app/server"]
