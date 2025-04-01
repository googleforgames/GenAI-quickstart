create schema if not exists "smartnpc";
CREATE TABLE IF NOT EXISTS smartnpc.player(
    player_id VARCHAR(1024) PRIMARY KEY,
    game_id VARCHAR(36) DEFAULT NULL,
    background TEXT DEFAULT NULL,
    class TEXT DEFAULT NULL,
    class_level int DEFAULT 1,
    name TEXT DEFAULT NULL,
    status TEXT DEFAULT NULL,
    lore_level int DEFAULT 1
);
GRANT USAGE ON SCHEMA smartnpc TO llmuser;
GRANT SELECT ON smartnpc.player TO llmuser;
