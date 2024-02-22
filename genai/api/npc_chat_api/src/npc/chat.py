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

def npcs_from_world(world, genai, db):
    return [ NPC(entity, genai, db) for entity in world['base'] if entity['entity_type'] == 1 ]

class NPC(object):
    _FIRST_HAND = """
You know the following:
{first_hand}
"""
    _SECOND_HAND = """

You trust the following things you've heard:
{second_hand}
"""

    def __init__(self, entity, genai, db):
        self._id = entity['entity_id']
        self._name = entity['entity_name']
        self._context = entity['context']
        self._db = db
        self._genai = genai

        # TODO: Are these global? Per NPC?
        self._knowledge_distance = 0.3
        self._knowledge_limit = 3
        self._chat_window = 6 # must be even, need last response to be ours at least for chat-bison

    def _format_context(self, knowledge):
        first_hand, second_hand = [], []
        for known in knowledge:
            who, what = known['provenance'], known['knowledge']
            if who:
                second_hand.append(f"* {who} said: {what}")
            else:
                first_hand.append(f"* {what}")
        relevant = self._FIRST_HAND.format(first_hand='\n'.join(first_hand)) if first_hand else ""
        relevant += self._SECOND_HAND.format(second_hand='\n'.join(second_hand)) if second_hand else ""
        return self._context.format(relevant=relevant)

    def _chat_history(self, from_id):
        return [{
            "author": "user" if chat['entity_id'] == from_id else "bot",
            "content": chat['message'],
        } for chat in self._db.get_chat_history(self._id, from_id, self._chat_window)]

    def reply(self, from_id, from_name, message):
        embedding = self._genai.get_embeddings([message])[0]
        knowledge = self._db.get_knowledge(self._id, embedding, self._knowledge_distance, self._knowledge_limit)
        context = self._format_context(knowledge)
        chat_history = self._chat_history(from_id)
        response = self._genai.send_message(context, chat_history, message)
        self._db.insert_chat(from_id, from_name, self._id, self._name, [message, response])

        return {"knowledge": knowledge, "context": context, "chat_history": chat_history, "response": response}
