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

# Base Image
FROM python:3.11.5

WORKDIR /workspace/frontend
COPY app.py /workspace/frontend
COPY requirements.txt /workspace/frontend
COPY templates/index.html /workspace/frontend/templates/

# Install Dependencies
RUN pip install -r requirements.txt

# Expose Port
EXPOSE 5000

# Start the Application
CMD ["python", "app.py"]
