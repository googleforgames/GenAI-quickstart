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
from datetime import datetime
from swagger_client.rest import ApiException
import time
import logging  # Import the logging module
import random
import requests
import base64
import os
import swagger_client as Agones
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = f'{int(random.random()*100000000)}'
socketio = SocketIO(app)

# create an instance of the API class
PORT=os.environ.get("AGONES_SDK_HTTP_PORT","8080")
conf = Agones.Configuration()
conf.host = "http://localhost:"+PORT

player_prompt = {}
player_guess = {}

logging.basicConfig(level=logging.INFO)  # Set to logging.DEBUG for more verbose logs 
logger = logging.getLogger(__name__)  # Get a logger for your application

headers = {"Content-Type": "application/json"}

logger.info('gameserver started')
logger.info('Agones SDK port: %s', PORT)

body = Agones.SdkEmpty() # SdkEmpty
agones = Agones.SDKApi(Agones.ApiClient(conf))
agones.health(body)

retry = 5
while retry != 0:
    try:
        retry = retry - 1
        agones.ready(body)
        break
    except:
        time.sleep(2)
        logger.info('retry connection')

def agones_health():
    while True:
        try:
            agones.health(body)
            time.sleep(0.3)
            logger.info('health check passed')
            print(datetime.now())
        except ApiException as exc:
            logger.info('health check failed')
            logger.info(exc)

health_thread = threading.Thread(target=agones_health)
health_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

game_round = 3
embedding_endpoint = 'http://embeddings-api'

@socketio.on('guess1')
def handle_message(data):
    player_id = request.sid
    message = data['message']
    oppontent_id = data['opponentId']
    round = int(data['round'])

    logger.info('Received guess %s from player %s for oppontent %s: %s', str(round), player_id, oppontent_id, message)

    if player_guess.get(player_id) is None:
        player_guess[player_id] = {}
    player_guess[player_id][round] = {
        'guess': message
    }
    
    # Send next picture
    if round != game_round:
        next_round = round + 1
        while player_prompt[oppontent_id][next_round]['picture'] is None:
            time.sleep(0.1)
        emit('llm_response', {'image': player_prompt[oppontent_id][next_round]['picture'], 'opponentId': oppontent_id, 'round': next_round}, room=player_id)
        logger.info('Sent image %s to %s', str(next_round), player_id)

    # Generate and store the picture for the guess
    guess_payload = {
        'prompt': f'''{message}''',
    }
    model_response = requests.post(f'http://genai-api.genai.svc/genai/image', headers=headers, json=guess_payload)
    # stable diffusion
    #model_response_cur = requests.post(f'http://stable-diffusion-api.genai.svc/generate', headers=headers, json=payload_cur)
    encoded_image = base64.b64encode(model_response.content).decode('utf-8')
    logger.info('Encoded guess image %s for player %s: %s', str(round), player_id, encoded_image)

    player_guess[player_id][round]['guess_picture'] = encoded_image

    # Generate and store the similarity score
    # embedding_req = requests.post(
    #     url = embedding_endpoint,
    #     headers = headers,
    #     json = json,
    # )

    similarity_prompt = f'''calculate the vector similarity number between '{player_prompt[oppontent_id][round]['prompt']}' and '{player_guess[player_id][round]['guess']}' as number A,
                            Return number A in the format: A = '''
    
    similarity_payload = {
        'prompt': f'''{similarity_prompt}''',
    }

    similarity_response = requests.post(f'http://genai-api.genai.svc/genai/text', headers=headers, json=similarity_payload)
    logger.info(f'Similarity response: {similarity_response.text}')

    similarity_response_without_quota = similarity_response.text.strip('"')
    score = float(similarity_response_without_quota.split()[-1])

    logger.info(f'score: {score}')

    player_prompt[player_id][round]['guess_score'] = score

    # Generate and return summary once both players have guessed all 3 pictures

    if round == game_round:
        while len(player_guess) != 2:
            time.sleep(0.1)
        for player in player_guess:
            while len(player_guess[player]) != game_round:
                time.sleep(0.1)
            for round in player_guess[player]:
                while player_guess[player][round].get('guess_picture') is None:
                    time.sleep(0.1)
        for player in player_guess:
            for round in player_guess[player]:
                logger.debug('Sending guess picture of Player %s round %s to player %s', player, round, player_id)
                try:
                    emit('guess_response', {'image': player_guess[player][round]['guess_picture'], 'round': round}, room=player_id)
                except:
                    logger.exception('Error sending guess picture of Player %s round %s to player %s', player, round, player_id)

@socketio.on('prompt')
def handle_message(data):
    player_id = request.sid
    message = data['message']
    round = int(data['round'])
    logger.info('Received prompt %s from player %s: %s', str(round), player_id, message)

    if round == 1:
        player_prompt[player_id] = {
            1: {
                'prompt': f'''{message}''',
            }
        }
    else:
        player_prompt[player_id][round] = {
            'prompt': f'''{message}''',
        }

    picture_generate_payload = {
        'prompt': f'''{message}''',
    }
    model_response = requests.post(f'http://genai-api.genai.svc/genai/image', headers=headers, json=picture_generate_payload)
    # stable diffusion
    #model_response_cur = requests.post(f'http://stable-diffusion-api.genai.svc/generate', headers=headers, json=picture_generate_payload)
    encoded_image = base64.b64encode(model_response.content).decode('utf-8')
    logger.info('Encoded image %s for player %s: %s', str(round), player_id, encoded_image)

    player_prompt[player_id][round]['picture'] = encoded_image
    logger.info('Stored image %s for player %s: ', str(round), player_id)
    
    # The first picture should be displayed if both players have entered all their prompts
    # The first picture page should be displayed only if the picture is generated

    if round != game_round:
        return
    
    while len(player_prompt) != 2:
        time.sleep(0.1)
    for player in player_prompt:
        if player != player_id:
            while len(player_prompt[player]) != game_round:
                time.sleep(0.1)
            logger.info("I'm here")
            while 'picture' not in player_prompt[player][1]:
                time.sleep(0.25)
                logger.info('Waiting for image 1')
            emit('llm_response', {'image': player_prompt[player][1]['picture'], 'opponentId': player, 'round': 1}, room=player_id)
            logger.info('Sent image 1 to %s', player_id)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=7654)
