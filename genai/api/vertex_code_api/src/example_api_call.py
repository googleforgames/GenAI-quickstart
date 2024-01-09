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

import sys
import logging
import requests
import argparse

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

def test_endpoint(endpoint, prompt):
    
    req = requests.post(
        url = endpoint,
        headers = {"Content-Type": "application/json"},
        json = {'prompt': prompt},
    )
    
    logging.info(f'Status Code: {req.status_code}')
    logging.info(f'Response:    {req.text}')


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--endpoint", required=True, help="LLM Endpoint with route, such as http://localhost:7777/my_test_route")
    parser.add_argument("--prompt", required=True, help="LLM Prompt")
    args = parser.parse_args()
    
    test_endpoint(endpoint=args.endpoint, prompt=args.prompt)

