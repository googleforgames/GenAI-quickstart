create schema if not exists "smartnpc";
CREATE TABLE IF NOT EXISTS smartnpc.conversation_examples(
    example_id VARCHAR(1024) PRIMARY KEY,
    game_id VARCHAR(36) DEFAULT NULL,
    scene_id VARCHAR(1024) DEFAULT NULL,
    conversation_example TEXT DEFAULT NULL,
    is_activate BOOLEAN DEFAULT TRUE
);
GRANT USAGE ON SCHEMA smartnpc TO llmuser;
GRANT SELECT ON smartnpc.conversation_examples TO llmuser;
