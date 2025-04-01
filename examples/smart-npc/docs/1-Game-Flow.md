

```mermaid
sequenceDiagram

participant Game Frontend
participant API
participant Gemini

alt New Game
Game Frontend ->> Game Frontend: new_game()
Game Frontend ->> Smart NPC API: get_lineup(team.id)
Smart NPC API ->> Game Frontend: lineup
else Get Suggestions
Game Frontend ->> Game Frontend: get_linup(player team)
Game Frontend ->> Game Frontend: get_linup(computer team)
Game Frontend ->> Smart NPC API: get_tactic_suggestion(payload:{player lineup, computer lineup)
Smart NPC API ->> Smart NPC API: construct prompt(scene_id, player lineup, computer lineup)
Smart NPC API ->> Gemini: get response
Gemini -->> Smart NPC API: response:{outcomes, recommendations, tactics}
Smart NPC API -->> Game Frontend: response:{outcomes, recommendations, tactics}
else Simulation
Game Frontend ->> Game Frontend: simulate_at_bat()
Note over Game Frontend, Gemini: Repeat [Get Suggestions] and [Simulation]
end