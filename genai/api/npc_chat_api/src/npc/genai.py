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

import vertexai

from vertexai.language_models import TextEmbeddingModel, ChatModel, ChatMessage

def genai_from_config(cfg):
    if cfg['global']['genai'] == 'VertexAI':
        return VertexAI(cfg['global'], cfg['VertexAI'])
    raise Exception(f"Unknown genai config: {cfg['global']['genai']}")

class VertexAI(object):
    def __init__(self, gcfg, cfg):
        vertexai.init(project=gcfg['project'], location=gcfg['location'])
        self._embedding_model = TextEmbeddingModel.from_pretrained(cfg['embedding_model'])

        # TODO: allow for non-chat (standard generation) models, or should we just have a different genai class for them?
        self._chat_model = ChatModel.from_pretrained(cfg['chat_model'])

    def get_embeddings(self, strings):
        # TODO: Vertex API supports 'task_type': https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/text-embeddings#request_body
        # but it's not supported in the Vertex Python SDK: https://cloud.google.com/python/docs/reference/aiplatform/latest/vertexai.language_models.TextEmbeddingModel
        # Later, we could use `RETRIEVAL_DOCUMENT` for "base knowledge" and `RETRIEVAL_QUERY` for everything else.
        return [e.values for e in self._embedding_model.get_embeddings(strings, auto_truncate=False)]

    def send_message(self, context, chat_history, message):
        parameters = {
            "candidate_count": 1,
            "max_output_tokens": 1024,
            "temperature": 0.9,
            "top_p": 1
        }

        chat = self._chat_model.start_chat(context=context, message_history=[ChatMessage(**chat) for chat in chat_history])
        resp = chat.send_message(message, **parameters)
        return resp.text.strip()
