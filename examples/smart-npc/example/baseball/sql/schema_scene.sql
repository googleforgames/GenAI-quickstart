create schema if not exists "smartnpc";
CREATE TABLE IF NOT EXISTS smartnpc.scene(
    scene_id VARCHAR(1024) PRIMARY KEY,
    game_id VARCHAR(36) DEFAULT NULL,
    goal TEXT DEFAULT NULL,
    scene TEXT DEFAULT NULL,
    status TEXT DEFAULT NULL,
    npcs TEXT DEFAULT NULL,
    knowledge TEXT DEFAULT NULL,
    conv_example_id VARCHAR(1024) DEFAULT NULL
);
GRANT USAGE ON SCHEMA smartnpc TO llmuser;
GRANT SELECT ON smartnpc.scene TO llmuser;
