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

import tomllib

# Mounted as ConfigMaps in genai/api/npc_chat_api/k8s.yaml
CONFIG_PATH="/config/config.toml"
WORLD_PATH="/config/world.toml"

def data_from_file(path):
    with open(path, "rb") as f:
       return tomllib.load(f)
