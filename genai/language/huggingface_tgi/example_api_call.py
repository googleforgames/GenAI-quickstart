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

import argparse
import logging
import openai
import sys

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

def chat_endpoint(endpoint, system):
    client = openai.OpenAI(
        base_url=endpoint,
        api_key="NOT NEEDED"
    )

    messages=[{"role": "system", "content": system}] if system else []
    while True:
        try:
            message = input('>>> ')
        except EOFError:
            return

        messages.append({"role": "user", "content": message.strip()})

        completion = client.chat.completions.create(model="tgi", messages=messages)
        resp = completion.choices[0].message.content
        messages.append({"role": "assistant", "content": resp})
        print('<<<', resp)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--endpoint", required=True, help="LLM Endpoint with route, such as http://localhost:7777/my_test_route")
    parser.add_argument("--system", help="System prompt, if API supports it")
    args = parser.parse_args()
    chat_endpoint(args.endpoint, args.system)

