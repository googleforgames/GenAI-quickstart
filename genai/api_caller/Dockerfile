# Copyright 2024 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM python:3.11-slim

WORKDIR /app

# Install curl
RUN apt-get update; apt-get install -y curl

# download and installs Node.js (Need npm to install wscat)
RUN curl -fsSL https://deb.nodesource.com/setup_21.x | bash
RUN apt-get install -y nodejs
# Install websocket cat (for testing websocket connections)
RUN npm install -g wscat

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Install production dependencies. (Copy requirements early to cache this layer.)
COPY api_caller/requirements.txt /etc/pip_requirements.txt
RUN pip install --no-cache-dir -r /etc/pip_requirements.txt

COPY api/vertex_code_api/src/example_api_call.py vertex_code_api.py
COPY api/vertex_text_api/src/example_api_call.py vertex_text_api.py
COPY api/vertex_chat_api/src/example_api_call.py vertex_chat_api.py
COPY api/genai_api/src/example_api_call.py genai_api.py
COPY api/stable_diffusion_api/src/example_api_call.py stable_diffusion_api.py
COPY api/vertex_image_api/src/example_api_call.py vertex_image_api.py
COPY api/vertex_gemini_api/src/example_api_call.py vertex_gemini_api.py
COPY api/npc_chat_api/src/example_api_call.py npc_chat_api.py
COPY language/huggingface_tgi/example_api_call.py huggingface_tgi.py
COPY language/embeddings/src/example_api_call.py embeddings.py

ENTRYPOINT ["/bin/bash"]
