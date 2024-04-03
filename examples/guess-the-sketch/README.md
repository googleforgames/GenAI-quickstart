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

1. Follow the top-level README (ensure that the http://genai-api.genai.svc/genai/text 
   and http://genai-api.genai.svc/genai/image endpoints are running).
2. [Install Agones](https://agones.dev/site/docs/installation/install-agones/yaml/#installing-agones) in your cluster.
3. Install Guess the Sketch into your cluster:
```
cd ~/GenAI-quickstart/examples/guess-the-sketch
skaffold run --build-concurrency=0 --cache-artifacts=false
```
4. You can run the following to check the GameServer status
```
kubectl get gs
```
5. Once the GameServer is Ready, you can connect to the game through its IP Address and PORT using web browser,
and open two pages to mock two players.

### To switch from Imagen 2 back to Imagen (1)

Scale the Imagen 1 deployment up and scale the Imagen 2 deployment down:
```
kubectl scale -ngenai deployment/vertex-image-api-imagen-1 --replicas=1
kubectl scale -ngenai deployment/vertex-image-api-imagen-2 --replicas=0
```

(Vice-versa to switch back.)
