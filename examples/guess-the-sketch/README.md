## Guess the Sketch Demo App

This demo app illustrates a simple game that incorporates image generation
in a multiplayer scenario.

The gameplay is:
1. Each player will type in a prompt to generate an image.
1. Each player will be presented an image and asked to create a caption to
   describe it.
1. The players will be shown the original prompt and told how close their
   caption was.

### To run the demo

Follow the top-level README. At least the `http://genai-api.genai.svc/genai/text` and
`http://genai-api.genai.svc/genai/image` endpoints need to be running.

```
cd ~/GenAI-quickstart/examples/guess-the-sketch
skaffold run --build-concurrency=0
```

Once the pod is running, you can connect to the game by running:

```
kubectl port-forward svc/guess-the-sketch-app 5000:5000
```

and opening two pages in your web browser at http://localhost:5000/

