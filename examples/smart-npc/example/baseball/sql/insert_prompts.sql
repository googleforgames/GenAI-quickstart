delete from smartnpc.prompt_template;
-- ############################## --
--      GENERAL
-- ############################## --
INSERT INTO smartnpc.prompt_template(prompt_id, game_id, scene_id, prompt_template, is_activate)
VALUES (
'OUTPUT_FORMAT',
'baseball',
'default',
'"3-5 word state summary": chance% [10 value state array in the Input Format]

',
True
);


INSERT INTO smartnpc.prompt_template(prompt_id, game_id, scene_id, prompt_template, is_activate)
VALUES (
'INPUT_FORMAT',
'baseball',
'default',
'
You will be given current state in the following format:
[
runner on first (true | false),
runner on second (true | false),
runner on third (true | false),
balls (0,1,2,3),
strikes (0,1,2),
outs (0,1,2),
inning (0...12),
defensive score lead (offensive score - defensive score),
defensive team play style (0: conservative, 1: assertive, 2: aggressive),
offensive team play style (0: conservative, 1: assertive, 2: aggressive)
]',
True
);


-- ## Line up ## --
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

-- ## Tactic selection ## --
INSERT INTO smartnpc.prompt_template(prompt_id, game_id, scene_id, prompt_template, is_activate)
VALUES (
'NPC_CONVERSATION_SCENCE_GOAL_TEMPLATE',
'baseball',
'TACTICS_SELECTION',
'

# SYSTEM
This is a baseball management video game where one player is controlling the home team and
another the away team. The player controls what the team does by selecting what
the coach will tell the batter or pitcher for each at-bat.

## YOUR TASKS

Based on the current game state and statistics, create options for the coaching
scripts that the video game displays to the players. Each script should be 20-40
words and advocate for a distinctly different
approach to the current at-bat that makes sense given the current state of the
baseball game.  For each combination of the batting and pitching tactics,
generate a valid possible outcome of the current at-bat if the players select that
combination of tactics.  Outcomes must represent the entire at-bat, and will
always result in either a hit or an out. Be sure to double-check that the
outcome makes sense given the rules of baseball.

Also create a meta-level tutorial script for each player, telling them which option
they should choose and why.


## Output
Taking into account the pitcher and batter statics and current state of the
game, make 3 pitching tactics scripts, and 3 batting tactics scripts. For each
of the 9 possible batting + pitching tactics combinations, generate a possible
outcome of the current at-bat that results. If you refer to a team member in a
script, be sure to use their last name.

## IMPORT RULES

Finally, In the voice of a friendly video game tutorial text box, explain to the
player controlling the pitching team how to select a pitching tactic, which
tactic you think they should select, and why (~50 words) Using the same
approach, also explain how to select a batting tactic to the player controlling
the batting team.  Do not refer to tactic indicies in the script, because those are 
an implementation detail the players don''t know about.

## OUTPUT FORMAT
Use this json schema for the tactics scripts and possible outcomes:
{TACTICS_OUTPUT_SCHEMA}

Here is a table describing each part of the JSON schema:

{TACTICS_OUTPUT_SCHEMA_DESCRIPTION}

Don''t include any headers or additional explanation outside of this output format.
',
True
);

INSERT INTO smartnpc.prompt_template(prompt_id, game_id, scene_id, prompt_template, is_activate)
VALUES (
'TACTICS_OUTPUT_SCHEMA_DESCRIPTION',
'baseball',
'TACTICS_SELECTION',
'
Element Name	Type	Description
tactics	object	Contains the pitching and batting tactic scripts.
tactics.pitching	array	An array of strings, where each string is a pitching tactic script that advances the goals of the pitcher.
tactics.batting	array	An array of strings, where each string is a batting tactic script that advances the goals of the pitcher.
outcomes	object	A map where keys are strings representing the pitching and batting tactic indices (e.g., "0.0", "0.1", etc.) and values are objects describing the outcome of the at-bat.
outcomes[key].outcome	string	A string describing the play that occurred (e.g., "Flyout to Center Field").
outcomes[key].game_state	object	An object describing the state of the game after the at-bat, if this outcome were to occur.
outcomes[key].game_state.r1	boolean	true if a runner is on first base; false otherwise.
outcomes[key].game_state.r2	boolean	true if a runner is on second base; false otherwise.
outcomes[key].game_state.r3	boolean	true if a runner is on third base; false otherwise.
outcomes[key].game_state.outs	integer	The number of outs after the play.
outcomes[key].game_state.runs	integer	The number of runs scored as a result of this play.
outcomes[key].title	string	A brief description of the outcome (e.g., "Ground ball double play").
recommendations	object	Contains the video game tutorial coach''s recommended pitching and batting tactics and rationales.
recommendations.pitching	object	Contains a game tutorial for selecting the recommended pitching tactic.
recommendations.pitching.index	integer	The index (starting from 0) of the recommended pitching tactic within the tactics.pitching array.
recommendations.pitching.script	string	The tutorial text script explaining the recommended pitching tactic.
recommendations.batting	object	Contains a game tutorial for selecting the recommended batting tactic.
recommendations.batting.index	integer	The index (starting from 0) of the recommended batting tactic within the tactics.batting array.
recommendations.batting.script	string	The tutorial text explaining the recommended batting tactic.
',
True
);


INSERT INTO smartnpc.prompt_template(prompt_id, game_id, scene_id, prompt_template, is_activate)
VALUES (
'TACTICS_OUTPUT_SCHEMA',
'baseball',
'TACTICS_SELECTION',
'
{
  "type": "object",
  "properties": {
    "tactics": {
      "type": "object",
      "properties": { "pitching": { "type": "array", "items": { "type": "string" } }, "batting": { "type": "array", "items": { "type": "string" } } },
      "required": ["pitching", "batting"]
    },
    "outcomes": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "outcome": { "type": "string" },
          "game_state": {
            "type": "object",
            "properties": {
              "r1": { "type": "boolean" },
              "r2": { "type": "boolean" },
              "r3": { "type": "boolean" },
              "outs": { "type": "integer" },
              "runs": { "type": "integer" }
            },
            "required": ["r1", "r2", "r3", "outs", "runs"]
          },
          "title": { "type": "string" }
        },
        "required": ["outcome", "game_state", "title"]
      }
    },
    "recommendations": {
      "type": "object",
      "properties": {
        "pitching": {
          "type": "object",
          "properties": { "index": { "type": "integer" }, "script": { "type": "string" } },
          "required": ["index", "script"]
        },
        "batting": {
          "type": "object",
          "properties": { "index": { "type": "integer" }, "script": { "type": "string" } },
          "required": ["index", "script"]
        }
      },
      "required": ["pitching", "batting"]
    }
  },
  "required": ["tactics", "outcomes", "recommendations"]
}

const exampleTopOfFirstResponse = {
  "tactics": {
    "pitching": [
      "Work the corners, keep it low and away. He''s a righty power hitter, so avoid letting him extend his arms.",
      "Mix up your pitches. Throw some fastballs inside to jam him, then come back with breaking balls away to keep him off balance.",
      "Try to get ahead in the count. If you get to 0-2, throw a slider or changeup. He may be looking fastball early."
    ],
    "batting": [
      "Be patient, Joseph. Green has a high walk rate. Don''t be afraid to take a walk if he''s not throwing strikes. First at-bat, see what he''s got.",
      "Look for a fastball early in the count. He''s likely to try and establish his fastball. Be ready to jump on it.",
      "Try to work the count. Green has given up a lot of hits. The deeper you get into the at-bat, the more likely you are to find a pitch you can hit."
    ]
  },
  "outcomes": {
    "0.0": {
      "outcome": "Strikeout looking.",
      "game_state": {
        "r1": false,
        "r2": false,
        "r3": false,
        "outs": 1,
        "runs": 0
      },
      "title": "Strikeout"
    },
    "0.1": {
      "outcome": "Groundout to second base.",
      "game_state": {
        "r1": false,
        "r2": false,
        "r3": false,
        "outs": 1,
        "runs": 0
      },
      "title": "Groundout"
    },
    "0.2": {
      "outcome": "Walk.",
      "game_state": {
        "r1": true,
        "r2": false,
        "r3": false,
        "outs": 0,
        "runs": 0
      },
      "title": "Walk"
    },
    "1.0": {
      "outcome": "Foul tip, strike three.",
      "game_state": {
        "r1": false,
        "r2": false,
        "r3": false,
        "outs": 1,
        "runs": 0
      },
      "title": "Strikeout"
    },
    "1.1": {
      "outcome": "Line drive single to left field.",
      "game_state": {
        "r1": true,
        "r2": false,
        "r3": false,
        "outs": 0,
        "runs": 0
      },
      "title": "Single"
    },
    "1.2": {
      "outcome": "Flyout to center field.",
      "game_state": {
        "r1": false,
        "r2": false,
        "r3": false,
        "outs": 1,
        "runs": 0
      },
      "title": "Flyout"
    },
    "2.0": {
      "outcome": "Swinging strikeout.",
      "game_state": {
        "r1": false,
        "r2": false,
        "r3": false,
        "outs": 1,
        "runs": 0
      },
      "title": "Strikeout"
    },
    "2.1": {
      "outcome": "Ground ball to shortstop, out at first.",
      "game_state": {
        "r1": false,
        "r2": false,
        "r3": false,
        "outs": 1,
        "runs": 0
      },
      "title": "Groundout"
    },
    "2.2": {
      "outcome": "Double to left field.",
      "game_state": {
        "r1": false,
        "r2": true,
        "r3": false,
        "outs": 0,
        "runs": 0
      },
      "title": "Double"
    }
  },
  "recommendations": {
    "pitching": "Pitching tactic 0: Work the corners.  This catcher has some power, so keep the ball away from his sweet spot.",
    "batting": "Batting tactic 1: Be patient. The pitcher walks a lot of guys. Let him work and try to get on base."
  }
}
',
True
);

-- ###############
--  Streaming
-- ###############

-- get tactic suggestions - streaming
INSERT INTO smartnpc.scene(scene_id, game_id, scene, status, goal, npcs, knowledge, conv_example_id)
VALUES (
'TACTICS_SELECTION_20250317_011',
'baseball',
'
You are a helpful senior manager in a baseball team.
You provide tactics suggestions and possible outcomes to the manager.
',
'ACTIVATE',
'
Based on the given current state, provide your predictions.
',
'',
'',
'default'
);

INSERT INTO smartnpc.prompt_template(prompt_id, game_id, scene_id, prompt_template, is_activate)
VALUES (
'STREAMING_GET_SUGGESTIONS',
'baseball',
'TACTICS_SELECTION_20250317_011',
'# SYSTEM
This is a baseball management video game where one player is controlling the home team and
another the away team. The player controls what the team does by selecting what
the coach will tell the batter or pitcher for each at-bat.

## YOUR TASKS

Based on the current game state and statistics, create options for the coaching
scripts that the video game displays to the players. Each script should be 20-40
words and advocate for a distinctly different
approach to the current at-bat that makes sense given the current state of the
baseball game.  For each combination of the batting and pitching tactics,
generate a valid possible outcome of the current at-bat if the players select that
combination of tactics. Outcomes must represent the entire at-bat and will
always result in either a hit or an out. Be sure to double-check that the
outcome makes sense given the rules of baseball.

Also create a meta-level tutorial script for each player, telling them which option
they should choose and why.

## Output
Taking into account the pitcher and batter statics and current state of the
game, make 3 pitching tactics scripts, and 3 batting tactics scripts. For each
of the 9 possible batting + pitching tactics combinations, generate a possible
outcome of the current at-bat that results. If you refer to a team member in a
script, be sure to use their last name.

## IMPORT RULES

Finally, In the voice of a friendly video game tutorial text box, explain to the
player controlling the pitching team how to select a pitching tactic, which
tactic you think they should select, and why (~50 words) Using the same
approach, also explain how to select a batting tactic to the player controlling
the batting team.  Do not refer to tactic indicies in the script, because those are
an implementation detail the players don''t know about.

## IMPORTANT

*   When generating the outcome of an at-bat, consider the current game state (runners on base, outs, score) and ensure the outcome is logically consistent. For example:
    *   A walk with the bases loaded MUST result in a run scored and the runner on first advancing to second, the runner on second advancing to third, and the runner on third scoring.  The number of outs MUST remain the same.
    *   A fly ball with runners on first and second and one out CANNOT be a sacrifice fly.
    *   The outcome **MUST BE VALIDATE**, for example, double play isn''t valid if no runner on base.
    *   If there are 2 outs, any play that results in the batter being out MUST also result in the end of the inning.
    *   If a runner is on first, a walk MUST result in the runner on first advancing to second.
    *   If a runner is on second, a sacrifice fly is impossible.
*   **Game End Condition**:
    *   The game ends when the home team is winning after the away team finishes batting in the top of the 9th inning.
    *   The game ends when the home team is ahead at the end of any subsequent inning after the 9th.
    *   If the home team is batting in the bottom of the 9th inning (or any extra inning) and takes the lead, the game is over immediately.
*   **About Home Runs**:
    *   A home run with no runners on base results in 1 run scored and no outs recorded.
    *   If the home team hits a home run in the bottom of the 9th inning or later to take the lead, the game ends immediately, and the number of outs should reflect the state before the home run.
    *   If there are already two outs, home run does not cause 3 outs.
    *   **A home run NEVER results in an out.** This is extremely important. The batter and any runners on base always score.
*   **About other plays**:
    *   If the batter hits the ball but reaches first base due to a fielding error, the number of outs does not increase.
    *   A foul ball should always results in an out. Because this is a per `at-bat` outcome. a at-bat with foul ball outcome should always indicates an out.
    * **Fielder''s Choice:** If the batter hits a ground ball and a fielder attempts to get a runner out at a base other than first, but fails, the batter is safe at first. This is scored as a fielder''s choice.  Runners may advance, and the number of outs remains the same *unless* the attempt at an out results in the third out.
*   **About ending the inning:**
    *   If there are already two outs, and the at-bat results in an out, you MUST indicate that the inning is over in the outcome (e.g., "Groundout to first base, inning over."). The number of outs MUST be 3.
    *   If there are fewer than two outs, and the at-bat results in a double play, you MUST indicate that the inning is over in the outcome (e.g., "Double play, inning over"). The number of outs MUST be 3.
    *   **Crucially, if there are two outs and the current at-bat does NOT result in an out, the inning MUST continue (outs remain at 2), and runners should advance appropriately based on the outcome of the play.**  For example, a single will put the batter on first.  A double will put the batter on second.  A walk will put the batter on first and force other runners to advance.
*   **About Walks:**
    *   A walk always puts the batter on first base.
    *   A walk **does not** result in an out.
    *   If there is a runner on first, a walk forces that runner to advance to second.
    *   If there are runners on first and second, a walk forces the runner on second to advance to third and the runner on first to advance to second, and the batter is on first.
    *   **If the bases are loaded (runners on first, second, and third), a walk MUST result in a run being scored, and all runners advance one base.**  This is a crucial rule; ensure the `runs` value in the `game_state` is updated correctly. After a walk with bases loaded, remember to set `r3` to `false`
*   **About Sacrifice Flies:**
    *   A runner on second or first cannot advance to home with a sacrifice fly.
    *   If a runner on third is on the base and the batter hits a flyout, the runner on third will score.
*   **Inning Over:**
    *   Inning is over *ONLY* when the 3rd out occurs.
*   **About Double Play:**
    *   Double plays are only possible if there is a runner on first base.
    *   If there are 2 outs, and the at-bat results in a double play, you MUST indicate that the inning is over in the outcome (e.g., "Double play, inning over"). The number of outs MUST be 3.
* **Advancing Runners:** When a batter gets a hit (single, double, triple), runners on base MUST advance the appropriate number of bases. A single advances each runner one base. A double advances each runner two bases. A triple advances each runner three bases.
* **Runs Scored**: Remember that runs are only scored when a player crosses home plate.  A groundout or flyout *does not* score a run unless a runner is on third and tags up (for a flyout) or is forced home (e.g., bases loaded walk). A single, double, or triple only scores runs if runners are in position to reach home plate. Carefully track runs scored.

## OUTPUT FORMAT
Use this json schema for output, split each parts by a tag: <tactics>, <recommendations> and <outcomes>.
<tactics>
{
  "type": "object",
  "properties": {
    "tactics": {
      "type": "object",
      "properties": { "pitching": { "type": "array", "items": { "type": "string" } }, "batting": { "type": "array", "items": { "type": "string" } } },
      "required": ["pitching", "batting"]
    }
}
</tactics>
<recommendations>
{
  "type": "object",
  "properties": {
    "recommendations": {
      "type": "object",
      "properties": {
        "pitching": {
          "type": "object",
          "properties": { "index": { "type": "integer" }, "script": { "type": "string" } },
          "required": ["index", "script"]
        },
        "batting": {
          "type": "object",
          "properties": { "index": { "type": "integer" }, "script": { "type": "string" } },
          "required": ["index", "script"]
        }
      },
      "required": ["pitching", "batting"]
    }
  },
  "required": ["tactics", "outcomes", "recommendations"]
}
</recommendations>
<outcomes>
{
  "type": "object",
  "properties": {
    "outcomes": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "outcome": { "type": "string" },
          "game_state": {
            "type": "object",
            "properties": {
              "r1": { "type": "boolean" },
              "r2": { "type": "boolean" },
              "r3": { "type": "boolean" },
              "outs": { "type": "integer" },
              "runs": { "type": "integer" }
            },
            "required": ["r1", "r2", "r3", "outs", "runs"]
          },
          "title": { "type": "string" }
        },
        "required": ["outcome", "game_state", "title"]
      }
    }
}
</outcomes>


Example:
<tactics>
{
  "tactics": {
    "pitching": [
      "Work the corners, keep it low and away. He''s a righty power hitter, so avoid letting him extend his arms.",
      "Mix up your pitches. Throw some fastballs inside to jam him, then come back with breaking balls away to keep him off balance.",
      "Try to get ahead in the count. If you get to 0-2, throw a slider or changeup. He may be looking fastball early."
    ],
    "batting": [
      "Be patient, Joseph. Green has a high walk rate. Don''t be afraid to take a walk if he''s not throwing strikes. First at-bat, see what he''s got.",
      "Look for a fastball early in the count. He''s likely to try and establish his fastball. Be ready to jump on it.",
      "Try to work the count. Green has given up a lot of hits. The deeper you get into the at-bat, the more likely you are to find a pitch you can hit."
    ]
  }
}
</tactics>
<recommendations>
{
  "recommendations": {
    "pitching": "Pitching tactic 0: Work the corners.  This catcher has some power, so keep the ball away from his sweet spot.",
    "batting": "Batting tactic 1: Be patient. The pitcher walks a lot of guys. Let him work and try to get on base."
  }
}
</recommendations>
<outcomes>
{
  "outcomes": {
    "0.0": {
      "outcome": "Strikeout looking.",
      "game_state": {
        "r1": false,
        "r2": false,
        "r3": false,
        "outs": 1,
        "runs": 0
      },
      "title": "Strikeout"
    },
    "0.1": {
      "outcome": "Groundout to second base.",
      "game_state": {
        "r1": false,
        "r2": false,
        "r3": false,
        "outs": 1,
        "runs": 0
      },
      "title": "Groundout"
    },
    "0.2": {
      "outcome": "Walk.",
      "game_state": {
        "r1": true,
        "r2": false,
        "r3": false,
        "outs": 0,
        "runs": 0
      },
      "title": "Walk"
    },
    "1.0": {
      "outcome": "Foul tip, strike three.",
      "game_state": {
        "r1": false,
        "r2": false,
        "r3": false,
        "outs": 1,
        "runs": 0
      },
      "title": "Strikeout"
    },
    "1.1": {
      "outcome": "Line drive single to left field.",
      "game_state": {
        "r1": true,
        "r2": false,
        "r3": false,
        "outs": 0,
        "runs": 0
      },
      "title": "Single"
    },
    "1.2": {
      "outcome": "Flyout to center field.",
      "game_state": {
        "r1": false,
        "r2": false,
        "r3": false,
        "outs": 1,
        "runs": 0
      },
      "title": "Flyout"
    },
    "2.0": {
      "outcome": "Swinging strikeout.",
      "game_state": {
        "r1": false,
        "r2": false,
        "r3": false,
        "outs": 1,
        "runs": 0
      },
      "title": "Strikeout"
    },
    "2.1": {
      "outcome": "Ground ball to shortstop, out at first.",
      "game_state": {
        "r1": false,
        "r2": false,
        "r3": false,
        "outs": 1,
        "runs": 0
      },
      "title": "Groundout"
    },
    "2.2": {
      "outcome": "Double to left field.",
      "game_state": {
        "r1": false,
        "r2": true,
        "r3": false,
        "outs": 0,
        "runs": 0
      },
      "title": "Double"
    }
  }
}
</outcomes>

Here is a table describing each part of the output schema:

Element Name    Type    Description
tactics object  Contains the pitching and batting tactic scripts.
tactics.pitching        array   An array of strings, where each string is a pitching tactic script that advances the goals of the pitcher.
tactics.batting array   An array of strings, where each string is a batting tactic script that advances the goals of the pitcher.
outcomes        object  A map where keys are strings representing the pitching and batting tactic indices (e.g., "0.0", "0.1", etc.) and values are objects describing the outcome of the at-bat.
outcomes[key].outcome   string  A string describing the play that occurred (e.g., "Flyout to Center Field"). The outcome **MUST BE VALIDATE**, for example, double play isn''t valid if no runner on base. If the outcome resulting an out, you must explictly indicate Out in the outcome string.
outcomes[key].game_state        object  An object describing the state of the game after the at-bat, if this outcome were to occur.
outcomes[key].game_state.r1     boolean true if a runner is on first base; false otherwise.
outcomes[key].game_state.r2     boolean true if a runner is on second base; false otherwise.
outcomes[key].game_state.r3     boolean true if a runner is on third base; false otherwise.
outcomes[key].game_state.outs   integer The number of outs after the play.
outcomes[key].game_state.runs   integer The number of runs scored as a result of this play.
outcomes[key].title     string  A brief description of the outcome (e.g., "Ground ball double play").
recommendations object  Contains the video game tutorial coach''s recommended pitching and batting tactics and rationales.
recommendations.pitching        object  Contains a game tutorial for selecting the recommended pitching tactic.
recommendations.pitching.index  integer The index (starting from 0) of the recommended pitching tactic within the tactics.pitching array.
recommendations.pitching.script string  The tutorial text script explaining the recommended pitching tactic. Simply give the explaination, DO NOT include any index number, jus talk like a coach to player.
recommendations.batting object  Contains a game tutorial for selecting the recommended batting tactic.
recommendations.batting.index   integer The index (starting from 0) of the recommended batting tactic within the tactics.batting array.
recommendations.batting.script  string  The tutorial text explaining the recommended batting tactic.

Don''t include any headers or additional explanation outside of this output format.

',
True
);
