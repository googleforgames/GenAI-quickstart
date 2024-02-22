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
import json
import logging
import requests
import argparse

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

def message_endpoint(endpoint, message=""):
    
    req = requests.post(
        url = endpoint,
        headers = {"Content-Type": "application/json"},
        json = {'message': message} if message else None,
    )

    logging.info(f'Status Code: {req.status_code}')
    logging.info(f'Response:    {req.text}')

def chat_endpoint(endpoint):
    while True:
        try:
            message = input('>>> ')
        except EOFError:
            return

        req = requests.post(
            url = endpoint,
            headers = {"Content-Type": "application/json"},
            json = {'message': message},
        )

        if req.status_code != 200:
            print(f'request failed: {req}')
            return

        resp = json.loads(req.text)
        print('<<<', resp['response'])


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--endpoint", required=True, help="LLM Endpoint with route, such as http://localhost:7777/my_test_route")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--chat', action='store_true', help="Interactive chat mode")
    mode.add_argument("--message", help="Chat message to send to NPC, JSON response logged")
    mode.add_argument("--empty", action='store_true', help="POST with no payload")
    args = parser.parse_args()
    
    if args.chat:
        chat_endpoint(endpoint=args.endpoint)
    elif args.empty:
        message_endpoint(endpoint=args.endpoint, message=args.message)
    else:
        message_endpoint(endpoint=args.endpoint, message=args.message)
