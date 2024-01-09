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

from flask import Flask, redirect, render_template, request, jsonify, session
import datetime
import json
import os, sys
import re
import random
import requests
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)

app = Flask(__name__)
app.config['SECRET_KEY'] = f'{int(random.random()*100000000)}'

GENAI_API_ENDPOINT = os.environ['GENAI_API_ENDPOINT']

headers = {"Content-Type": "application/json"}

####################################################
#
#   Routes
#
####################################################

@app.route('/genai_health')
def health_check():
    return jsonify({'status': 'ok'})


@app.route('/')
def index():
    return redirect("npc_character")


@app.route('/npc_character')
def npc_character():
    return render_template("npc_character.html")


@app.route('/npc_character_chatbot', methods=['POST'])
def npc_character_chatbot():
    request_payload = request.get_json()
    logging.debug(f'\nrequest payload: {request_payload}')

    if request_payload['updateCharacter']:
        context = 'Your role is to introduce the newly added character to the chat group.'
    else:
        context = f'''You are {request_payload['characterContext']}. 
You should respond to all questions in the persona of {request_payload['characterContext']}. You never refer to yourself as a chatbot or AI.
'''

    if 'chatHistory' in request_payload:
        context += f"\nHere the chat history for {request_payload['characterContext']} that can be used when answering questions:\n"
        seen_chat = []
        for chat in request_payload['chatHistory']:
            if chat not in seen_chat:
                if chat["sender"].upper() in ['USER', request_payload['characterName'].upper()]:
                    context += f'{chat["sender"].upper()}: {chat["message"]}\n'
                    seen_chat.append(chat)

    payload = {
        'prompt': f'''{request_payload["message"]}''',
        'context': context,
    }

    logging.debug(f'Prompt:  {payload["prompt"]}')
    logging.debug(f'Context: {payload["context"]}')

    model_response = requests.post(f'{GENAI_API_ENDPOINT}/genai/chat', headers=headers, json=payload)

    if model_response.status_code != 200:
        logging.warn(f'Response code: {model_response.status_code}. {model_response.text}')
        return {}

    formatted_response = (model_response.text).replace('\n','<br>').replace('"','')

    response = {
        'reply': formatted_response,
        'characterName': request_payload['characterName'],
    }

    logging.debug(f'LLM Response Payload: {response}')

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)

