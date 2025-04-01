create schema if not exists "smartnpc";
CREATE TABLE IF NOT EXISTS smartnpc.rosters(
    team_id VARCHAR(256) NOT NULL,
    session_id VARCHAR(256),
    player_id VARCHAR(1024) NOT NULL,
    roster TEXT DEFAULT NULL,
    PRIMARY KEY (team_id, session_id)
);
GRANT USAGE ON SCHEMA smartnpc TO llmuser;
GRANT SELECT ON smartnpc.rosters TO llmuser;
