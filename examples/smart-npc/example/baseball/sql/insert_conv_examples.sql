delete from smartnpc.conversation_examples;
INSERT INTO smartnpc.conversation_examples(
    example_id,
    game_id,
    scene_id,
    conversation_example,
    is_activate)
VALUES (
'default',
'baseball',
'default',
'

**Current state is:** [false, false, true, 2, 3, 2, 7, 2, 0, 2]
**Possible next states:**
* batter strikes out: 35% [false, false, false, 0, 0, 0, 8, -2, 0, 2]
(batter strikes out, current inning ends, so clear out balls / strikes and outs, advance to next inning.)
* single, RBI: 15% [true, false, false, 0, 0, 2, 7, 1, 0, 2]
(single and RBI, runner on first, clear out balls and strikes, 2 outs in 7 inning.)
* batter walks: 15% [true, false, true, 0, 0, 2, 7, 2, 1, 1]
(walks, better to first, runner on third, clear out balls and strikes, outs no change.)
* fly out: 15% [false, false, false, 0, 0, 0, 8, -2, 1, 1]
(walks, better to first, runner on third, clear out balls and strikes, outs no change.)


**Current state is:** [false, false, true, 2, 3, 1, 7, 2, 0, 2]
**Possible next states:**
* batter strikes out: 35% [false, false, true, 0, 0, 2, 7, 2, 0, 2]
(batter strikes out, current inning ends, so clear out balls / strikes and outs, advance to next inning.)
* single, RBI: 15% [true, false, false, 0, 0, 1, 7, 1, 0, 2]
(single and RBI, runner on first, clear out balls and strikes, 2 outs in 7 inning.)
* batter walks: 15% [true, false, true, 0, 0, 1, 7, 2, 1, 1]
(walks, better to first, runner on third, clear out balls and strikes, outs no change.)
* Home run: 15% [false, false, false, 0, 0, 1, 7, 0, 1, 1]
(home run, runner + batter = 2 RBI, clear out balls and strikes, outs no change.)

',
True
);
