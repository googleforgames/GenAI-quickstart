create schema if not exists "smartnpc";
CREATE TABLE IF NOT EXISTS smartnpc.prompt_template(
    prompt_id VARCHAR(1024) NOT NULL,
    game_id VARCHAR(36) DEFAULT NULL,
    scene_id VARCHAR(1024) NOT NULL,
    prompt_template TEXT DEFAULT NULL,
    is_activate BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (scene_id, prompt_id)
);
GRANT USAGE ON SCHEMA smartnpc TO llmuser;
GRANT SELECT ON smartnpc.prompt_template TO llmuser;
