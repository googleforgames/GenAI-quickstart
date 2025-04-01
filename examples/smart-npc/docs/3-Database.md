# Database

Key tables for the baseball simulation games are:

| Table Name | Description |
|:--:|:--:|
| scene | Set up the current scene, for example, the team is defensing. |
| prompts | Prompt database |


## Table Schema

This section explains table design.

### Scene

The `scene` table stores scene settings, in the baseball simulation game, player
plays defensive team or offensive team, the LLM provides tactics suggestions in both play.

The `defensive team` and `offensive team` are two scenes in the game. Other scene like
`creating lineup`.

* Table schema

```sql
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
```

* Sample data

```sql
INSERT INTO smartnpc.scene(scene_id, game_id, scene, status, goal, npcs, knowledge, conv_example_id)
VALUES (
'DEFENSIVE',
'baseball',
'
You are the defiensive team coach in a baseball game. You have to determine what to do next.
',
'ACTIVATE',
'
Based on the given current state, think of possible next states.
',
'',
'',
'default'
);
```

### Prompts

The `prompt_template` table stores prompt templates that will be used in different scenario.
For example, when the player as the deffensive team, is expecting suggestions from the LLM what's
the best next action to prevent the offensive team from gaining runs.

While in a offensive team scene, the player needs advises on how to drive runs. Each scene may use
different prompts with different statistic to get proper suggestions from the LLM.

* Table schema

```sql

CREATE TABLE IF NOT EXISTS smartnpc.prompt_template(
    prompt_id VARCHAR(1024) NOT NULL,
    game_id VARCHAR(36) DEFAULT NULL,
    scene_id VARCHAR(1024) NOT NULL,
    prompt_template TEXT DEFAULT NULL,
    is_activate BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (scene_id, prompt_id)
);
```

* Sample data

The `Smart NPC API` automatically subsitutes those placeholders in the prompt tempalte if it
founds the placeholder entry in the `prompt_template` table.

```sql
INSERT INTO smartnpc.prompt_template(prompt_id, game_id, scene_id, prompt_template, is_activate)
VALUES (
'NPC_CONVERSATION_SCENCE_GOAL_TEMPLATE',
'baseball',
'LINEUP_SUGGESTIONS',
'# SYSTEM
You are an in-game coach of a baseball simulation game.
You will be given rosters of matching teams,
base on the roster, you create the lineup for your team.

## Your Tasks

1. You will be given roster of both teams.

2. **Base on the roster** create the lineup for your team.
    * Carefully examine the roster to generate lineup that has best chance to win.

## Output Format

{LINEUP_OUTPUT_FORMAT}

## Important
* Do not include headers, explanations, or extraneous information.
* Walkthrough the roster information.
* Think step by step, make sure the lineup is valid.

',
True
);

INSERT INTO smartnpc.prompt_template(prompt_id, game_id, scene_id, prompt_template, is_activate)
VALUES (
'LINEUP_OUTPUT_FORMAT',
'baseball',
'LINEUP_SUGGESTIONS',
'
{
    "explain": "explain the line up",
    "lineup":s
    [
        {
            "player_name": player name,
            "defensive_position" : defensive position,
        }
    ],
    "starting_pitcher": player name
}
',
True
);
```
