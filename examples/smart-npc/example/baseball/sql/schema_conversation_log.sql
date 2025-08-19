create schema if not exists "smartnpc";
CREATE TABLE IF NOT EXISTS smartnpc.conversation_logs(
    conversation_id VARCHAR(256) PRIMARY KEY,
    game_id VARCHAR(36) DEFAULT NULL,
    session_id VARCHAR(256),
    scene_id VARCHAR(1024),
    player_id VARCHAR(1024),
    npc_id VARCHAR(1024),
    conversation_log TEXT DEFAULT NULL,
    date_time TEXT DEFAULT NULL,
    status TEXT DEFAULT NULL,
    start_gametime TEXT DEFAULT NULL,
    end_gametime TEXT DEFAULT NULL,
    summary TEXT DEFAULT NULL
);
GRANT USAGE ON SCHEMA smartnpc TO llmuser;
GRANT SELECT ON smartnpc.conversation_logs TO llmuser;
