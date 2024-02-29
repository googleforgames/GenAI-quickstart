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

from json import loads

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

def dot(v1, v2):
   return sum(i[0] * i[1] for i in zip(v1, v2))

def test_endpoint(endpoint, prompts, model):
    json = {'prompts': prompts}
    if model:
        json['model'] = model

    req = requests.post(
        url = endpoint,
        headers = {"Content-Type": "application/json"},
        json = json,
    )

    logging.info(f'Status Code: {req.status_code}')
    logging.info(f'Response:    {req.text}')

    if req.status_code != 200 or len(prompts) <= 1:
        logging.info(f'(not showing similarity - error or too few prompts)')
        return

    embeddings = loads(req.text)
    embeddings = list(zip(embeddings['prompts'], embeddings['embeddings']))
    for i in range(len(embeddings)):
        for j in range(i+1, len(embeddings)):
            d = dot(embeddings[i][1], embeddings[j][1])
            logging.info(f'Dot product similarity between "{embeddings[i][0]}" and "{embeddings[j][0]}": {d}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--endpoint", required=True, help="LLM Endpoint with route, such as http://localhost:7777/my_test_route")
    parser.add_argument("--prompt", required=True, help="LLM Prompt (repeated - embeddings in order of args)", nargs='+', default=[])
    parser.add_argument("--model", default="sentence-transformers/multi-qa-MiniLM-L6-cos-v1", help="Sentence transformer model to use")
    args = parser.parse_args()

    test_endpoint(endpoint=args.endpoint, prompts=args.prompt, model=args.model)

