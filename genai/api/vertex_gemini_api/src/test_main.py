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

# pytest -s -W ignore

from fastapi.testclient import TestClient
from unittest import mock
import json
from main import app

client = TestClient(app)

@mock.patch('requests.post')
def test_genai(mock_post):

    # Define a mock response content as a JSON string
    expected_response = {'mocked_key': 'mocked_value'}
    mock_response_content = json.dumps(expected_response).encode()

    # Create a mock response object with the necessary attributes
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.content = mock_response_content

    # Set the mock object to the patched function
    mock_post.return_value = mock_response

    # Payload for the POST request
    payload = {
        "prompt": "test prompt",
        "max_output_tokens": 1024,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40
    }

    # Make a request to your API
    response = client.post("/", json=payload)

    # Assertions
    assert response.status_code == 200
    assert response.json() == expected_response
    mock_post.assert_called_once()

