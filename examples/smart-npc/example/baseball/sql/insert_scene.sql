delete from smartnpc.scene;

-- get tactic suggestions
INSERT INTO smartnpc.scene(scene_id, game_id, scene, status, goal, npcs, knowledge, conv_example_id)
VALUES (
'TACTICS_SELECTION',
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


-- get lineup suggestions
INSERT INTO smartnpc.scene(scene_id, game_id, scene, status, goal, npcs, knowledge, conv_example_id)
VALUES (
'LINEUP_SUGGESTIONS',
'baseball',
'
You are the baseball team coach in a baseball game.
You create lineup for the game.
',
'ACTIVATE',
'
Based on the given roster of your team and the opponent team,
Create a line up for your team.
',
'',
'',
'default'
);


-- get tactic suggestions - streaming
INSERT INTO smartnpc.scene(scene_id, game_id, scene, status, goal, npcs, knowledge, conv_example_id)
VALUES (
'TACTICS_SELECTION_20250313',
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