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

import json
import requests
import base64
from io import BytesIO
from diffusers import StableDiffusionPipeline
import torch


class Stable_Diffusion:

    def __init__(self, model_type):
        # Model Type should reference a image generation model from HuggingFace.
        # https://huggingface.co/models
        # Example MODEL_TYPE = 'runwayml/stable-diffusion-v1-5'
        self.model_type = model_type
        
        # Load Model
        self.pipe = StableDiffusionPipeline.from_pretrained(self.model_type, torch_dtype=torch.float16)
        self.pipe = self.pipe.to("cuda")


    def get_image(self, prompt, num_inference_steps=50, guidance_scale=7.5):
        try:
            image = self.pipe(prompt, num_inference_steps=num_inference_steps, guidance_scale=guidance_scale).images[0]

            # Process and format image
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            image_bytes = buffer.getvalue()            

            return image_bytes
        except Exception as e:
            print(f'[ EXCEPTION ] {e}')
            return ''
