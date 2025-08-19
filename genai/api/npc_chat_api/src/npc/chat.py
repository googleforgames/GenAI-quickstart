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

import logging

def npcs_from_world(world, genai, db):
    return [ NPC(entity, genai, db) for entity in world['base'] if entity['entity_type'] == 1 ]

class NPC(object):
    _KNOWN = """
- You know the following:
{first_hand}
"""
    _FIRST_HAND = """

- You've said the following to other people related to this topic:
{second_hand}
"""
    _SECOND_HAND = """

- You've heard the following from other people related to this topic, but you're not sure if you trust it:
{second_hand}
"""

    def __init__(self, entity, genai, db):
        self._id = entity['entity_id']
        self._name = entity['entity_name']
        self._context = entity['context']
        self._db = db
        self._genai = genai

        # TODO: Are these global? Per NPC?
        self._knowledge_distance = 0.5
        self._knowledge_limit = 3
        self._chat_window = 10 # must be even, need last response to be ours
        self._max_prompt_bytes = 6500 # how much we can send to the LLM - we trim from chat history if necessary
        self._per_chat_cost = 10 # bytes to "charge" for each chat

    def _format_context(self, knowledge):
        facts, first_hand, second_hand = [], [], []
        for known in knowledge:
            who, what = known['provenance'], known['knowledge']
            if who == "I":
                first_hand.append(f"* {who} said: {what}")
            elif who:
                second_hand.append(f"* {who} said: {what}")
            else:
                facts.append(f"* {what}")
        relevant = self._KNOWN.format(first_hand='\n'.join(facts)) if facts else ""
        relevant += self._FIRST_HAND.format(second_hand='\n'.join(first_hand)) if first_hand else ""
        relevant += self._SECOND_HAND.format(second_hand='\n'.join(second_hand)) if second_hand else ""
        return self._context.format(relevant=relevant)

    def _chat_history(self, from_id, max_bytes):
        chats = [{
            "author": "user" if chat['entity_id'] == from_id else "bot",
            "content": chat['message'],
        } for chat in self._db.get_chat_history(self._id, from_id, self._chat_window)]
        while sum([len(chat['content']) + self._per_chat_cost for chat in chats]) > max_bytes:
            chats = chats[2:]
        logging.info(f'using {len(chats)}/{self._chat_window} chat messages')
        return chats

    def reply(self, from_id, from_name, message):
        embedding = self._genai.get_embeddings([message])[0]
        knowledge = self._db.get_knowledge(self._id, embedding, self._knowledge_distance, self._knowledge_limit)
        context = self._format_context(knowledge)
        chat_history = self._chat_history(from_id, self._max_prompt_bytes - len(context) - len(message))
        response = self._genai.send_message(context, chat_history, message)
        self._db.insert_chat(from_id, from_name, self._id, self._name, [message, response])

        return {"knowledge": knowledge, "context": context, "chat_history": chat_history, "response": response}
