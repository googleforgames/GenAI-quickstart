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

import json
import logging
import requests
import vertexai

from vertexai.language_models import TextEmbeddingModel, ChatModel, ChatMessage

def genai_from_config(cfg):
    if cfg['global']['genai'] == 'VertexAI':
        return VertexAI(cfg['global'], cfg['VertexAI'])
    elif cfg['global']['genai'] == 'GKEGenAI':
        return GKEGenAI(cfg['global'], cfg['GKEGenAI'])
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

class GKEGenAI(object):
    def __init__(self, gcfg, cfg):
        self._embeddings_endpoint = cfg['embeddings_endpoint']
        self._embeddings_model = cfg['embeddings_model']

        if cfg['completions'] == 'ChatCompletions':
            self._completions = GKEGenAI.ChatCompletions(cfg['ChatCompletions'])
        elif cfg['completions'] == 'ChatCompletionTemplate':
            self._completions = GKEGenAI.ChatCompletionTemplate(cfg['ChatCompletionTemplate'])
        else:
            raise ValueError(f'GKEGenAI.completions unknown or invalid: "{cfg["completions"]}"')

    def get_embeddings(self, prompts):
        params = {'prompts': prompts, 'model': self._embeddings_model}

        resp = requests.post(
            url=self._embeddings_endpoint,
            headers={'Content-Type': 'application/json'},
            json=params,
        )
        resp.raise_for_status()
        embeddings = json.loads(resp.text)
        return embeddings['embeddings']

    def send_message(self, context, chat_history, message):
        return self._completions.send_message(context, chat_history, message)

    @staticmethod
    def _translate_messages(context, chat_history, message, supports_system):
        if supports_system:
            messages = [{'role': 'system', 'content': context}]
        else:
            # TODO: This is awkward, but not all models support the system message (e.g. gemma-7b and mixtral)
            messages = [{'role': 'user', 'content': context}, {'role': 'assistant', 'content': 'OK'}]

        for chat in chat_history:
            messages.append({
                'role': 'user' if chat['author'] == 'user' else 'assistant',
                'content': chat['content'],
            })
        assert messages[-1]['role'] == 'assistant' # last message in history should be bot
        messages.append({'role': 'user', 'content': message})

        return messages

    class ChatCompletions(object):
        def __init__(self, cfg):
            import openai
            self._chat_completions = openai.OpenAI(base_url=cfg['endpoint'], api_key="NOT NEEDED").chat.completions
            self._chat_model = cfg['model']
            self._use_system_for_context = cfg['use_system_for_context']
            self._params = cfg['params']

        def send_message(self, context, chat_history, message):
            completions = self._chat_completions.create(
                model=self._chat_model,
                messages=GKEGenAI._translate_messages(context, chat_history, message, self._use_system_for_context),
                **self._params
            )
            assert len(completions.choices) == 1
            return completions.choices[0].message.content

    class ChatCompletionTemplate(object):
        def __init__(self, cfg):
            self._endpoint = cfg['endpoint']

            from jinja2 import Template
            self._chat_template = Template(cfg['chat_template'])
            self._use_system_for_context = cfg['use_system_for_context']

        def send_message(self, context, chat_history, message):
            prompt=self._chat_template.render(
                messages=GKEGenAI._translate_messages(context, chat_history, message, self._use_system_for_context),
                add_generation_prompt=True,
            )

            resp = requests.post(
                url=self._endpoint,
                headers={'Content-Type': 'application/json'},
                json={
                    'inputs': prompt,
                    'parameters': { 'temperature': 0.9, 'max_new_tokens': 1024 },
                },
            )
            resp.raise_for_status()
            resp = json.loads(resp.text)
            return resp['generated_text']
