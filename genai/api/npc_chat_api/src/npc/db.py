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

import itertools

from google.cloud import spanner

def db_from_config(cfg, genai):
    if cfg['global']['database'] == 'Spanner':
        return Spanner(genai, cfg['global'], cfg['Spanner'])
    raise Exception(f"Unknown database config: {cfg['global']['database']}")

class Spanner(object):
    _CHAT_HISTORY = """\
SELECT
  EntityId,
  EventDescription
FROM EntityHistoryDynamic
WHERE
  (EntityId = @entityId1 AND TargetEntityId = @entityId2) OR (EntityId = @entityId2 AND TargetEntityId = @entityId1)
ORDER BY EventTime DESC, MessageId DESC
LIMIT @limit
"""

    _KNOWLEDGE = """
WITH maybeRelevant AS (
    -- maybeRelevant is a union of "known facts" by @entityId, and world facts (entity 0),
    -- plus anything @entityId said or heard in chat. The `Provenance` column indicates who
    -- relayed the fact, with NULL meaning "It is known".
    SELECT
        EventDescription,
        NULL as Provenance,
        EventDescriptionEmbedding,
        COSINE_DISTANCE(EventDescriptionEmbedding, @embedding) as Distance
    FROM EntityHistoryBase
    WHERE EntityId = 0 OR EntityId = @entityId
    --
    -- TODO: The following part of the query attempts to incorporate "learned" knowledge.
    -- However, we need a safety/quality layer to incorporate this, for a couple reasons:
    --   * Griefers abound, and it's easy to "re-ground" the NPC on fake knowledge.
    --   * Without fine tuning, it's easy for models to "break character" and
    -- UNION ALL
    -- SELECT
    --     EventDescription,
    --     IF(EntityId = @entityId, "I", EntityName) as Provenance,
    --     EventDescriptionEmbedding,
    --     COSINE_DISTANCE(EventDescriptionEmbedding, @embedding) as Distance
    -- FROM EntityHistoryDynamic
    -- WHERE EntityId = @entityId OR TargetEntityId = @entityId
), withinDistance AS (
    -- withinDistance filters the relevant pieces down to a maximum distance and structures
    -- the event for bucketing, below.    
    SELECT
        STRUCT(EventDescription as EventDescription, Provenance as Provenance) as Data,
        Distance
    FROM maybeRelevant
    WHERE Distance < @distance
), bucketed AS (
    -- bucketed implements a form of "minimum distance" anti-crowding: we partition the
    -- results up into buckets of size 1/@crowdBuckets, e.g. 0.1, and pick an arbitrary one
    -- from each bucket. This helps the diversity of knowledge returned.
    SELECT
        ANY_VALUE(Data) as Data,
        ANY_VALUE(Distance) as Distance
    FROM withinDistance
    GROUP BY CAST(Distance * @crowdBuckets AS INT64)
)
SELECT
  Data.EventDescription as EventDescription,
  Data.Provenance as Provenance,
  Distance
FROM bucketed
ORDER BY Distance
LIMIT @limit
"""

    def __init__(self, genai, gcfg, cfg):
        self._get_embeddings = genai.get_embeddings
        self._db = spanner.Client().instance(cfg['instance_id']).database(cfg['database_id'])

    # TODO: This is doing one-by-one insert into the batch, but is getting called in a loop. Be kinder?
    @staticmethod
    def _batch_insert(batch, table, column_values: dict):
        columns, values = list(zip(*column_values.items()))
        batch.insert(table, columns=columns, values=[values])

    def _insert_base(self, batch, event_counter, base_event):
        descs = base_event['events']
        embeddings = self._get_embeddings(descs)

        for (desc, embedding) in zip(descs, embeddings):
            Spanner._batch_insert(batch, 'EntityHistoryBase', {
                'EntityId': base_event['entity_id'],
                'EventId': next(event_counter),
                'EntityName': base_event['entity_name'],
                'EntityType': base_event['entity_type'],
                'EventDescription': desc,
                'EventDescriptionEmbedding': embedding,
            })

    def _insert_chat(self, batch, message_counter, chat_event):
        descs = chat_event['chat_history']
        embeddings = self._get_embeddings(descs)
        speakers = ((chat_event['entity_id'], chat_event['entity_name']), (chat_event['target_entity_id'], chat_event['target_entity_name']))

        for (i, desc, embedding) in zip(range(len(descs)), descs, embeddings):
            source, target = speakers[i % 2], speakers[(i+1) % 2] # alternate who is speaking
            Spanner._batch_insert(batch, 'EntityHistoryDynamic', {
                'EntityId': source[0],
                'EventTime': spanner.COMMIT_TIMESTAMP,
                'MessageId': next(message_counter),
                'EntityName': source[1],
                'EntityType': chat_event['entity_type'],
                'TargetEntityId': target[0],
                'TargetEntityName': target[1],
                'EventDescription': desc,
                'EventDescriptionEmbedding': embedding,
            })

    def get_chat_history(self, entity_id1, entity_id2, limit):
        with self._db.snapshot() as snapshot:
            rows = snapshot.execute_sql(
                self._CHAT_HISTORY,
                params={
                    'entityId1': entity_id1,
                    'entityId2': entity_id2,
                    'limit': limit,
                },
                param_types={
                    'entityId1': spanner.param_types.INT64,
                    'entityId2': spanner.param_types.INT64,
                    'limit': spanner.param_types.INT64,
                },
            )
            return list([{'entity_id': row[0], 'message': row[1]} for row in reversed(list(rows))])

    def insert_chat(self, entity_id, entity_name, target_entity_id, target_entity_name, messages):
        with self._db.batch() as batch:
            self._insert_chat(batch, itertools.count(), {
                'entity_id': entity_id,
                'entity_name': entity_name,
                'entity_type': 1, # NPC
                'target_entity_id': target_entity_id,
                'target_entity_name': target_entity_name,
                'chat_history': messages,
            })

    def get_knowledge(self, entity_id, embedding, distance, limit, crowd_buckets=10):
        with self._db.snapshot() as snapshot:
            knowledge = snapshot.execute_sql(
                self._KNOWLEDGE,
                params={
                    'entityId': entity_id,
                    'embedding': embedding,
                    'distance': distance,
                    'limit': limit,
                    'crowdBuckets': crowd_buckets,
                },
                param_types={
                    'entityId': spanner.param_types.INT64,
                    'embedding': spanner.param_types.Array(spanner.param_types.FLOAT64),
                    'distance': spanner.param_types.FLOAT64,
                    'limit': spanner.param_types.INT64,
                    'crowdBuckets': spanner.param_types.INT64,
                },
            )
            return [{'knowledge': row[0], 'provenance': row[1], 'distance': row[2]} for row in knowledge]

    def reinitialize(self, data):
        with self._db.batch() as batch:
            batch.delete("EntityHistoryBase", spanner.KeySet(all_=True))
            batch.delete("EntityHistoryDynamic", spanner.KeySet(all_=True))

            event_counter = itertools.count()
            for base_event in data['base']:
                self._insert_base(batch, event_counter, base_event)

            message_counter = itertools.count()
            for chat_event in data['chat']:
                self._insert_chat(batch, message_counter, chat_event)
