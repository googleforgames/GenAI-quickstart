## REST API Flow

```mermaid
sequenceDiagram

Game Frontend ->> Smart NPC API: request
Smart NPC API ->> Quick Start dispatcher endpoint: request
Quick Start dispatcher endpoint ->> Vertex Chat API: request
Vertex Chat API -->> Quick Start dispatcher endpoint: response
Quick Start dispatcher endpoint -->> Smart NPC API: response
Smart NPC API -->>Game Frontend: response
```

## Websocket / Streaming API Flow

```mermaid
sequenceDiagram

Game Frontend ->> Smart NPC API: streaming request
Smart NPC API ->> Smart NPC API: construct prompt
Smart NPC API -->> Gemini API: generate response
Gemini API -->> Smart NPC API: response
Smart NPC API -->>Game Frontend: response
```
