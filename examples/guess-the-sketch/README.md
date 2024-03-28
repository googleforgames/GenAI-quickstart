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

Then Follow the [instruction](https://agones.dev/site/docs/installation/install-agones/yaml/#installing-agones)
to install Agones in your cluster

Then run:

```
cd ~/GenAI-quickstart/examples/guess-the-sketch
skaffold run --build-concurrency=0 --cache-artifacts=false
```

You can run the following to check the GameServer status
```
kubectl get gs
```

Once the GameServer is Ready, you can connect to the game through its IP Address and PORT using web browser,
and open two pages to mock two players.
