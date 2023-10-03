# Copyright 2023 Google LLC All Rights Reserved.
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

import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_llm_get():
    prompt = "test prompt"
    response = client.get(f"/llm?prompt={prompt}")
    assert response.status_code == 200
    assert isinstance(response.text, str)

def test_llm_post():
    prompt = {"prompt": "test prompt"}
    response = client.post("/llm", json=prompt)
    assert response.status_code == 200
    assert isinstance(response.text, str)

def test_invalid_llm_get():
    response = client.get("/llm")
    assert response.status_code == 422
    #assert response.json() == {"error": "Invalid text prompt"}

def test_invalid_llm_post():
    response = client.post("/llm", json={})
    assert response.status_code == 422
    #assert response.json() == {"error": "Invalid text prompt"}
