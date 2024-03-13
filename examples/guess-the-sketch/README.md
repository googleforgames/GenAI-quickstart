## Guess the Sketch Demo App

This demo app illustrates a simple game that incorporates image generation
in a multiplayer scenario.

The gameplay is:
1. Each player will type in a prompt to generate an image.
1. Each player will be presented an image and asked to create a caption to
   describe it.
1. The players will be shown the original prompt and told how close their
   caption was.


### To build the demo

```
# These steps will already be done if you followed the top-level readme
export PROJECT_ID=$(gcloud config list --format 'value(core.project)' 2>/dev/null)
export LOCATION=us-central1
export SKAFFOLD_DEFAULT_REPO=$LOCATION-docker.pkg.dev/$PROJECT_ID/repo-genai-quickstart

cd $CUR_DIR/examples/guess-the-sketch/src

docker build -f Dockerfile --tag=$SKAFFOLD_DEFAULT_REPO/guess-the-sketch:0.1 .
docker push $SKAFFOLD_DEFAULT_REPO/guess-the-sketch:0.1
```

### To run the demo

```
cd $CUR_DIR/examples/guess-the-sketch

sed "s:your-image-repo:$SKAFFOLD_DEFAULT_REPO:g" < k8s.yaml > k8s.yaml.new ; mv k8s.yaml.new k8s.yaml

kubectl apply -f k8s.yaml
```

Once the pod is running, you can connect to the game by running:

```
kubectl port-forward svc/guess-the-sketch-app 5000:5000
```

and opening two pages in your webbrowser at http://localhost:5000/

