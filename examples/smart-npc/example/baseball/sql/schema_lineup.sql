create schema if not exists "smartnpc";
CREATE TABLE IF NOT EXISTS smartnpc.lineup(
    team_id VARCHAR(256) NOT NULL,
    player_id VARCHAR(1024) NOT NULL,
    session_id VARCHAR(256),
    lineup TEXT DEFAULT NULL,
    PRIMARY KEY (team_id, player_id)
);
GRANT USAGE ON SCHEMA smartnpc TO llmuser;
GRANT SELECT ON smartnpc.lineup TO llmuser;
