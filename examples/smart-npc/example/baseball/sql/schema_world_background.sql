create schema if not exists "smartnpc";
CREATE TABLE IF NOT EXISTS smartnpc.world_background(
    background_id VARCHAR(1024) PRIMARY KEY,
    game_id VARCHAR(36) DEFAULT NULL,
    background_name TEXT DEFAULT NULL,
    content TEXT DEFAULT NULL,
    lore_level int DEFAULT 1,
    background_embeddings vector(768) NULL,
    background TEXT DEFAULT NULL
);
GRANT USAGE ON SCHEMA smartnpc TO llmuser;
GRANT SELECT ON smartnpc.world_background TO llmuser;
