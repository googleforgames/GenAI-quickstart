
# Smart NPC

The Smart NPC demonstrates using Gemini-1.5-Flash to
generate NPC dialogues while maintaining the character personality,
storyline and scene settings thorughout the conversation.

Players are expected to achieve an objective of the scene, Gemini simulate
involving NPCs to respond to the player while implicitly guiding the player
toward the objective.

## Baseball simulation demo game

This example using the concept of LLM powered Smart NPC in a baseball simulation game,
where the player plays the coach of a baseball team. The `NPC` which powered by the LLM
provides tactics suggestions to the player.

## Applicaiton Flow

[Smart NPC API flow](./docs/0-SmartNPC-API-Flow.md)

[Game flow](./docs/1-Game-Flow.md)

## Database Tables

[Database Tables](./docs/3-Database.md)

## Configurations

* [config.app.toml.template](./config.app.toml.template) contains the SQL queries for
game logics in the `baseball` section.

It also holds SQL queries for the framework itself in `sql` section.

* [const.py](./src/utils/const.py) determines if the game uses Google for Games Quick Start
as the LLM backend. Update the `USE_QUICK_START` to `False` to invoke Gemini 2.0 API directly.

## Deploy the Application

*   Deploy the application

```
cd $CUR_DIR/examples/smart-npc

export PROJECT_ID=$(gcloud config list --format 'value(core.project)' 2>/dev/null)

find . -type f -name "*.template.yaml" -exec \
  bash -c "template_path={}; sed \"s:your-unique-project-id:${PROJECT_ID:?}:g\" < \${template_path} > \${template_path/%.template.yaml/.yaml} " \;

skaffold run
```

*   Create database and ingest data

Use your PostgreSQL client of choice, execute [SQL scripts](./example/baseball/sql/) to create
database tables and insert data to the tables.
