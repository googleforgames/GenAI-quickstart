# Copyright 2023 Google LLC All Rights Reserved.
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

FROM nvidia/cuda:11.8.0-base-ubuntu22.04

RUN apt update && \
apt install -y software-properties-common && \
add-apt-repository ppa:deadsnakes/ppa && \
DEBIAN_FRONTEND=noninteractive apt-get -y install tzdata &&\
apt install -y python3.9 && \
apt install -y python3-pip

WORKDIR /app

# ENV vars should be passed in when starting container
ENV GCP_PROJECT_ID="" 
ENV MODEL_TYPE="" 

COPY requirements.txt main.py model_util.py /app/

# Install production dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# Start the application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
