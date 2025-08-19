create schema if not exists "smartnpc";
CREATE TABLE IF NOT EXISTS smartnpc.memory(
    memory_id VARCHAR(256) PRIMARY KEY,
    game_id VARCHAR(36) DEFAULT NULL,
    session_id VARCHAR(256),
    player_id VARCHAR(1024),
    npc_id VARCHAR(1024),
    summary TEXT DEFAULT NULL,
    date_time TEXT DEFAULT NULL,
    status TEXT DEFAULT NULL,
    memory_type TEXT DEFAULT NULL,
    gametime TEXT DEFAULT NULL
);
GRANT USAGE ON SCHEMA smartnpc TO llmuser;
GRANT SELECT ON smartnpc.memory TO llmuser;

