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

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import time
import logging  # Import the logging module
import random
import requests
import base64
import re
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = f'{int(random.random()*100000000)}'
socketio = SocketIO(app)

pending_requests = {}
original_prompts = {}

logging.basicConfig(level=logging.INFO)  # Set to logging.DEBUG for more verbose logs 
logger = logging.getLogger(__name__)  # Get a logger for your application

headers = {"Content-Type": "application/json"}

print("working directory: " + os.getcwd())
print("files in cwd: " +  ', '.join(os.listdir(os.getcwd())))

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('guess')
def handle_message(message):
    logger.info('Received guess: %s', message)
    pending_requests[request.sid]['guess'] = message
    partner_id = pending_requests[request.sid]['partner']

    if pending_requests[partner_id]['guess'] is None:
        emit('guess_response', {'message': 'Wait partner guess'}, room=request.sid)
    else:
        # Both partners have guessed
        emit('guess_response', {'message': 'You guessed: ' + message + ' - Your partner\'s original prompt was: ' + pending_requests[request.sid]['partner_message']}, room=request.sid)
        emit('guess_response', {'message': 'You guessed: ' + pending_requests[partner_id]['guess'] + ' - Your partner\'s original prompt was: ' + pending_requests[partner_id]['partner_message']}, room=partner_id)

        # Calculate similarity
        similarity_prompt = f'''calculate the vector similarity number between '{pending_requests[partner_id]['message']}' and '{pending_requests[request.sid]['guess']}' as number A, 
                            calculate the vector similarity number between '{pending_requests[request.sid]['message']}' and '{pending_requests[partner_id]['guess']}' as number B. 
                            Return number A and number B in the format: A = , B = ''' 
        payload_similarity = {
            'prompt': f'''{similarity_prompt}''',
        }

        logger.info(f'Similarity payload: {payload_similarity}')

        similarity_response_cur = requests.post(f'http://genai-api.genai.svc/genai/text', headers=headers, json=payload_similarity)

        # logger.info(f'Similarity response: {similarity_response_cur.text}')
        similarity_prompt_cur_without_quota = similarity_response_cur.text.strip('"')
        logger.info(f'Similarity response without quota: {similarity_prompt_cur_without_quota}')

        parts = similarity_prompt_cur_without_quota.split(",")  # Split the string by commas

        # Extract numbers and convert to float
        score1 = float(parts[0].split()[-1])  
        score2 = float(parts[1].split()[-1]) 

        logger.info(f'num1: {score1}')
        logger.info(f'num2: {score2}')

        if score1 > score2:
            emit('winner', {'message': 'You won!'}, room=request.sid)
            emit('winner', {'message': 'You lost!'}, room=partner_id)
        elif score1 < score2:
            emit('winner', {'message': 'You lost!'}, room=request.sid)
            emit('winner', {'message': 'You won!'}, room=partner_id)
        else:
            emit('winner', {'message': 'It\'s a tie!'}, room=request.sid)
            emit('winner', {'message': 'It\'s a tie!'}, room=partner_id)

        del pending_requests[request.sid]
        del pending_requests[partner_id]

@socketio.on('message')
def handle_message(message):
    request_id = request.sid
    logger.info('Received request %s', request_id)
    logger.info('socket id %s', request.sid)
    logger.info('Message: %s', message)
    logger.info('Pending requests: %s', pending_requests)

    # TODO ... (Timeout logic - Consider a background task or database) ...

    pending_requests[request_id] = {
        'timestamp': time.time(),
        'partner': None,
        'socket_id': request.sid,
        'message': message,
        'partner_message': None,
        'guess': None
    }

    for pending_id, pending_req in pending_requests.items():
        if pending_id != request_id and pending_req['partner'] is None: 
            # Match found!
            logging.info(f'Match found')
            pending_req['partner'] = request.sid
            pending_req['partner_message'] = message
            pending_requests[request_id]['partner'] = pending_id
            pending_requests[request_id]['partner_message'] = pending_req['message']
            payload_cur = {
                'prompt': f'''{message}''',
            }
            payload_pre = {
                'prompt': f'''{pending_req['message']}''',
            }
            # vertex
            model_response_cur = requests.post(f'http://genai-api.genai.svc/genai/image', headers=headers, json=payload_cur)
            model_response_pre = requests.post(f'http://genai-api.genai.svc/genai/image', headers=headers, json=payload_pre)
            # stable diffusion
            #model_response_cur = requests.post(f'http://stable-diffusion-api.genai.svc/generate', headers=headers, json=payload_cur)
            #model_response_pre = requests.post(f'http://stable-diffusion-api.genai.svc/generate', headers=headers, json=payload_pre)


            encoded_image_cur = base64.b64encode(model_response_cur.content).decode('utf-8')
            encoded_image_pre = base64.b64encode(model_response_pre.content).decode('utf-8')

            # Notify both clients with messages:
            emit('match_found', {'message': 'Match found - You initiated! Your partner id is ' + request_id}, room=pending_id)
            emit('llm_response', {'image': encoded_image_cur}, room=pending_id)
            emit('match_found', {'message': 'Match found! Your partner id is ' + pending_id}, room=request.sid)
            emit('llm_response', {'image': encoded_image_pre}, room=request.sid)

if __name__ == '__main__':
    socketio.run(app, debug=True)
