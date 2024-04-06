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
from flask_socketio import SocketIO, emit, join_room
from json import loads
from swagger_client.rest import ApiException
import time
import logging  # Import the logging module
import random
import requests
import base64
import os
import swagger_client as Agones
import threading

# Uncomment to use Stable Diffusion explicitly - requires the Stable Diffusion backend, which uses a GPU:
#   kubectl scale deployment/stable-diffusion-endpt --replicas=1 -ngenai
# IMAGE_GENERATION_ENDPOINT="http://stable-diffusion-api.genai.svc"

# Use whatever the GenAI API is routing to (default Vertex)
IMAGE_GENERATION_ENDPOINT="http://genai-api.genai.svc/genai/image"
EMBEDDINGS_ENDPOINT="http://embeddings-api.genai.svc/"
EMBEDDINGS_MODEL="sentence-transformers/multi-qa-MiniLM-L6-cos-v1"

app = Flask(__name__,
            static_folder="static")
app.config['SECRET_KEY'] = f'{int(random.random()*100000000)}'
socketio = SocketIO(app)

# create an instance of the API class
PORT=os.environ.get("AGONES_SDK_HTTP_PORT","9358")
conf = Agones.Configuration()
conf.host = "http://localhost:"+PORT

logging.basicConfig(level=logging.DEBUG)  # Set to logging.INFO for less verbose logs
logger = logging.getLogger(__name__)  # Get a logger for your application

headers = {"Content-Type": "application/json"}

logger.debug('gameserver started')
logger.debug('Agones SDK port: %s', PORT)

body = Agones.SdkEmpty() # SdkEmpty
agones = Agones.SDKApi(Agones.ApiClient(conf))
agones.health(body)

# Retry connection to Agones SDK for 5 times if it fails
retry = 5
while retry != 0:
    try:
        retry = retry - 1
        agones.ready(body)
        break
    except:
        time.sleep(2)
        logger.debug('retry connection')

def agones_health():
    while True:
        try:
            api_response = agones.health(body)
            # logger.debug('health check reponse: %s', api_response)
            time.sleep(2)
        except ApiException as exc:
            logger.error('health check failed: %s', exc)

health_thread = threading.Thread(target=agones_health)
health_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

LIMITED_PROMPTS = os.environ.get("LIMITED_PROMPTS", "false")
logger.debug('LIMITED_PROMPTS: %s', LIMITED_PROMPTS)

game_round = 3
embedding_endpoint = 'http://embeddings-api'
# The nested dictionary to store the prompts and pictures for each round of each player
# The outer dictionary is indexed by the player id, and the inner dictionary is indexed by the round number
player_prompt = {}
# The nested dictionary to store the guesses and pictures for each round of each player
# The outer dictionary is indexed by the player id, and the inner dictionary is indexed by the round number
player_guess = {}
# The set to store the players who have clicked the "New Game" button or disconnected for more than 30 seconds
dropped_players = set()
# The set to store the players who was assigned to the gameserver
connected_players = set()
# The set to store the players who is/was connected
player_history = set()
sid_to_player_id = {}
player_id_to_promptes_set = {}
full_connection_time = time.time()

def check_connection():
    while True:
        global full_connection_time
        try:
            # Retrieve the current GameServer data
            api_response = agones.get_game_server()
            logger.debug("GameServer status: %s", api_response.status.state)
            now = time.time()
            if api_response.status.state == "Allocated":
                logger.debug("Checking connection")
                logger.debug("Connected players: %s", len(connected_players))
                logger.debug("full_connection_time: %s", full_connection_time)
                if len(connected_players) != 2:
                    if now - full_connection_time > 60:
                        logger.debug("Not enough players on this server, shutdown the server")
                        agones.shutdown(body)
                else:
                    full_connection_time = now
                time.sleep(2)
            else:
                time.sleep(5)
                full_connection_time = now
        except ApiException as e:
            logger.warning("Exception when calling SDKApi->get_game_server: %s\n" % e)
            time.sleep(5)

check_connection_thread = threading.Thread(target=check_connection)
check_connection_thread.start()

@socketio.on('syncSession')
def handle_sync_session(data):
    player_id = data['playerId']
    logger.debug('Player %s: Received syncSession from sid %s', player_id, request.sid)
    if player_id in player_history:
        # A known player reconnected, i.e. refresh, for simiplicity, we just redirect to start page
        emit('redirect', room=request.sid)
    else:
        # New player
        if len(connected_players) == 2:
            logger.debug("too many players on this server, redirecting to frontend")
            emit('redirect', room=request.sid)
        else:
            logger.debug('Player %s added into connected_players', player_id)
            connected_players.add(player_id)
            player_history.add(player_id)
            sid_to_player_id[request.sid] = player_id
            join_room(player_id)
            player_id_to_promptes_set[player_id] = len(player_id_to_promptes_set) + 1
            emit('limited_prompts', {'limited': LIMITED_PROMPTS, 'player_num': player_id_to_promptes_set[player_id]}, room=player_id)

@socketio.on('disconnect')
def handle_disconnect():
    player_id = sid_to_player_id[request.sid]
    if player_id == None:
        return
    logger.debug('Player %s disconnected', player_id)
    connected_players.discard(player_id)

@socketio.on('exitGame')
def handle_message(data):
    player_id = sid_to_player_id[request.sid]
    logger.debug('Player %s: Received exitGame', player_id)
    dropped_players.add(player_id)
    # If both players have dropped, shutdown the gameserver
    if len(dropped_players) == 2:
        agones.shutdown(body)

# When player click "New Game" button
@socketio.on('playAgain')
def handle_message(data):
    player_id = sid_to_player_id[request.sid]
    logger.debug('Player: %s: Received playAgain', player_id)
    dropped_players.add(player_id)
    # If both players have dropped, shutdown the gameserver
    if len(dropped_players) == 2:
        agones.shutdown(body)

# When player submit the guess
@socketio.on('guess')
def handle_message(data):
    player_id = sid_to_player_id[request.sid]
    message = data['message']
    oppontent_id = data['opponentId']
    round = int(data['round'])

    logger.debug('Player %s: Received guess %s for opponent %s: %s', player_id, str(round), oppontent_id, message)
    encoded_image = "placeholder"
    if LIMITED_PROMPTS == "true":
        pass
    else:
        # Do moderation by generating the image from the guess
        guess_payload = {
            'prompt': f'''{message}''',
        }
        model_response = requests.post(IMAGE_GENERATION_ENDPOINT, headers=headers, json=guess_payload)
        if model_response.content == b'{}':
            emit('guess_image_generation_response', {'response': 'failure', 'round': round}, room=player_id)
            return
        encoded_image = base64.b64encode(model_response.content).decode('utf-8')

    emit('guess_image_generation_response', {'response': 'success', 'round': round}, room=player_id)
    # Store the guess
    if player_guess.get(player_id) is None:
        player_guess[player_id] = {}
    player_guess[player_id][round] = {
        'guess': message
    }

    player_guess[player_id][round]['guess_picture'] = encoded_image
    # Send the guess picture to both the players, they will be shown in summary page
    emit('guess_response', {'image': encoded_image, 'guess': message, 'round': round, 'from': 'myself'}, room=player_id)
    emit('guess_response', {'image': encoded_image, 'guess': message, 'round': round, 'from': 'other'}, room=oppontent_id)

    # Send next picture which is generated by the opponent's prompt
    if round != game_round:
        next_round = round + 1
        while player_prompt[oppontent_id][next_round]['picture'] is None:
            time.sleep(0.1)
        emit('guess_sketch_response', {'image': player_prompt[oppontent_id][next_round]['picture'], 'prompt': player_prompt[oppontent_id][next_round]['prompt'], 'opponentId': oppontent_id, 'round': next_round}, room=player_id)
        logger.debug('Player %s: Sent image %s', player_id, str(next_round))
    
    # Generate the similarity score and send to both players; they will be shown in summary page
    try:
        score = similarity(player_prompt[oppontent_id][round]['prompt'], player_guess[player_id][round]['guess'])
    except:
        logging.exception("similarity() failed")
        score = -0.99   # "-99%" still fits in the text box, but it's obviously a weird number.
    player_prompt[player_id][round]['guess_score'] = score

    # Send the score to both the players,
    emit('score_response', {'score': score, 'round': round, 'from': 'myself'}, room=player_id)
    emit('score_response', {'score': score, 'round': round, 'from': 'other'}, room=oppontent_id)

# When player submit the prompt for generating Sketch
@socketio.on('prompt')
def handle_message(data):
    player_id = sid_to_player_id[request.sid]
    message = data['message']
    round = int(data['round'])
    logger.debug('Player %s: Received prompt %s: %s', player_id, str(round), message)

    # Generate and store the picture for the prompt\
    picture_generate_payload = {
        'prompt': f'''{message}''',
    }
    model_response = requests.post(IMAGE_GENERATION_ENDPOINT, headers=headers, json=picture_generate_payload)
    # Send an empty image to indicate the picture generation failure
    error_handling = not LIMITED_PROMPTS
    if model_response.content == b'{}':
        emit('prompt_response', {'image': '', 'prompt': message, 'round': round, 'error_handling': error_handling}, room=player_id)
        return
    encoded_image = base64.b64encode(model_response.content).decode('utf-8')
    # Store the prompt and generated picture
    if player_prompt.get(player_id) is None:
        player_prompt[player_id] = {}
    player_prompt[player_id][round] = {
        'prompt': message
    }
    player_prompt[player_id][round]['picture'] = encoded_image

    # Send the generated picture back to the player, this will be shown in the summary page
    emit('prompt_response', {'image': encoded_image, 'prompt': message, 'round': round, 'error_handling': error_handling}, room=player_id)
    
    # Now check whether it's time to send the picture to the opponent for guessing
    # The first picture should be displayed if both players have entered all their prompts
    # The first picture page should be displayed only if the picture is generated
    if round != game_round:
        return
    logger.debug('Player %s: All prompts received', player_id)
    while len(player_prompt) != 2:
        time.sleep(0.1)
    for player in player_prompt:
        if player != player_id:
            while len(player_prompt[player]) != game_round:
                time.sleep(0.1)
            while 'picture' not in player_prompt[player][1]:
                time.sleep(0.1)
            # Send the first picture to the opponent for guessing
            emit('guess_sketch_response', {'image': player_prompt[player][1]['picture'], 'prompt': player_prompt[player][1]['prompt'], 'opponentId': player, 'round': 1}, room=player_id)

def similarity(p1, p2):
    '''Calculate dot product distance between two prompts'''

    resp = requests.post(
        url = EMBEDDINGS_ENDPOINT,
        headers = {"Content-Type": "application/json"},
        json = {'prompts': [p1, p2], 'model': EMBEDDINGS_MODEL},
        timeout=0.5,
    )
    resp.raise_for_status()

    embeddings = loads(resp.text)['embeddings']
    return dot(embeddings[0], embeddings[1])

def dot(v1, v2):
   return sum(i[0] * i[1] for i in zip(v1, v2))

if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0', port=7654)
