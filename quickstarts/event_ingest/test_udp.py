# Copyright 2023 Google LLC All Rights Reserved.
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

# NOTE: This script is used for testing. It can be removed or edited at anytime.

import json
import socket
import sys
import argparse
import time, datetime

def send_udp(json_payload, host, port):
    try:
        json_data = json.dumps(json_payload)
        server_address = (host, port)
        print(f'[ INFO ] Using Server Address: {server_address}')
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        sent_bytes = sock.sendto(json_data.encode(), server_address)
        print(f'Sent {sent_bytes} bytes to {server_address}')
        sock.close()
    except Exception as e:
        print(f'[ EXCEPTION ] {e}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, required=False, default="0.0.0.0", help='Event Ingest Service hostname or IP')
    parser.add_argument('--port', type=int, required=False, default=7777,      help='Event Ingest Service port')
    parser.add_argument('--data', type=str, required=False, default="",        help='Data to send to ML model')
    args = parser.parse_args()
    
    if args.data == "":
        print(f'Sending default data to {args.host}:{args.port}')
        data_payload = {
            "eventid": f'eventid_123{int(time.time())}',
            "eventtype": "spawn",
            "timestamp": int(time.time()),
            "playerid": "player1234",
            "label": "no label",
            "xcoord": 1.1,
            "ycoord": 1.1,
            "zcoord": 1.1,
            "dow": 4,
            "hour": 12,
            "score": 33,
            "minutesplayed": 30,
            "timeinstore": 15,
            "ml": "propensity_to_buy",
        }
    else:
        print(f'Sending your data to {args.host}:{args.port}')
        data_payload = json.loads(args.data)
    
    start_time = datetime.datetime.now()
    send_udp(json_payload=data_payload, host=args.host, port=args.port)
    runtime = (datetime.datetime.now() - start_time).total_seconds() * 1000 # milliseconds
    print(f'Runtime: {runtime} milliseconds')
