create schema if not exists "smartnpc";
CREATE TABLE IF NOT EXISTS smartnpc.teams(
    team_id VARCHAR(256) PRIMARY KEY,
    team_name VARCHAR(36) DEFAULT NULL,
    team_year int,
    description TEXT DEFAULT NULL,
    roster TEXT DEFAULT NULL,
    default_lineup TEXT DEFAULT NULL
);
GRANT USAGE ON SCHEMA smartnpc TO llmuser;
GRANT SELECT ON smartnpc.teams TO llmuser;

