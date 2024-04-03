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

import os
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

class Google_Cloud_Imagen:
    '''
    https://cloud.google.com/vertex-ai/docs/generative-ai/image/overview
    '''

    def __init__(self, GCP_PROJECT_ID, GCP_REGION, VERTEX_IMAGE_GENERATION_MODEL):
        if GCP_PROJECT_ID=="":
            print(f'[ WARNING ] GCP_PROJECT_ID ENV variable is empty. Be sure to set the GCP_PROJECT_ID ENV variable.')

        if GCP_REGION=="":
            print(f'[ WARNING ] GCP_REGION ENV variable is empty. Be sure to set the GCP_REGION ENV variable.')

        self.GCP_PROJECT_ID = GCP_PROJECT_ID
        self.GCP_REGION = GCP_REGION

        self.vertexai = vertexai.init(project=GCP_PROJECT_ID, location=GCP_REGION)
        self.model = ImageGenerationModel.from_pretrained(VERTEX_IMAGE_GENERATION_MODEL)
