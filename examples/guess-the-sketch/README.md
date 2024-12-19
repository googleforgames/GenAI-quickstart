## Guess the Sketch Demo App

This demo app illustrates a simple game that incorporates image generation
in a multiplayer scenario.

### Gameplay

1. Two players click the "Start button" game (if you want to test alone, use two browser windows)
1. Each player will be presented with 3 text boxes to enter prompts to generate images.
1. Players will be presented with images and asked to create captions to describe them.
1. Players will be shown a summary screen with all of the prompts and captions and a winner will declared!

_Note: There is an alternate mode for the game where instead of free-form prompt text boxes players are
presented with three predefined prompts and asked to select one of them._

### Installing the game

1. Follow the top-level README (ensure that the http://genai-api.genai.svc/genai/text 
   and http://genai-api.genai.svc/genai/image endpoints are running).
   - (optional) Scale down the deployments that aren't being used to reduce resource consumption:
   ```
    kubectl scale deployment npc-chat-api -n genai --replicas=0
    kubectl scale deployment huggingface-tgi-mistral-cpu -n genai --replicas=0
    kubectl scale deployment vertex-code-api -n genai --replicas=0
    kubectl scale deployment vertex-gemini-api -n genai --replicas=0
   ```
1. [Install Agones](https://agones.dev/site/docs/installation/install-agones/helm/#installing-the-chart) into your cluster.
1. Install the game server fleet into your cluster:
   - (optional) If you want to run the game mode with predefined prompts, update `examples/guess-the-sketch/Dockerfile` to set `LIMITED_PROMPTS` to `true` before running the `skaffold` command.
   ```
   cd ${CUR_DIR:?}/examples/guess-the-sketch
   skaffold run --build-concurrency=0 --cache-artifacts=false
   ```
1. Deploy Open Match 2 on Cloud Run by following [the documention](https://github.com/googleforgames/open-match2/blob/main/docs/DEVELOPMENT.md).
   - NOTE: before running `gcloud run services replace service.yaml` to deploy Open Match 2, make sure to:
      - Replace the IP address of the `OM_REDIS_WRITE_HOST` and `OM_REDIS_READ_HOST` in the [`service.yaml`](https://github.com/googleforgames/open-match2/blob/main/deploy/service.yaml) file to be the IP address of the Redis instance you created.
      - Replace the `run.googleapis.com/network-interfaces` field to use the network and subnetwork configured by terraform. In this case, it's `vpc-genai-quickstart` and `sn-usc1`.
      - Replace the `cloud.googleapis.com/location` field to be the location of your `sn-usc1` subnetwork (us-central1 if you followed the top level [README](https://github.com/googleforgames/GenAI-quickstart/blob/main/README.md)).
1. Configure Open Match 2's permissions to your cluster.
   - Create a Google Service Account in your project and give it the `Cloud Run Invoker` role.
   - Replace the value of `iam.gke.io/gcp-service-account` of `frontend_k8s.yaml` and `director_k8s.yaml` to be the Google Service Account you created.
   - Bind the Kubernetes Service Account in `frontend_k8s.yaml` and `director_k8s.yaml` to the Google Service Account(in the form of `SERVICE_ACCOUNT_NAME@PROJECT_ID.iam.gserviceaccount.com`) with 
   ```
   gcloud iam service-accounts add-iam-policy-binding   --role roles/iam.workloadIdentityUser   --member "serviceAccount:PROJECT_ID.svc.id.goog[genai/frontend-sa]"   YOUR_GOOGLE_SERVICE_ACCOUNT

   gcloud iam service-accounts add-iam-policy-binding   --role roles/iam.workloadIdentityUser   --member "serviceAccount:PROJECT_ID.svc.id.goog[genai/fleet-allocator]"   YOUR_GOOGLE_SERVICE_ACCOUNT
   ```
   - Replace the value of `OM_CORE_ADDRESS` environment variable in `frontend_k8s.yaml` and `director_k8s.yaml` to be the url of the OM2 that's deployed on Cloud Run.
1. Install the frontend and match maker into your cluster:
   - (optional) If you want to enable the consent screen, update `examples/guess-the-sketch/matchmaker/frontend/k8s.yaml` to set `showConsentPage` to `true` before running the `skaffold` command.
   ```
   cd ${CUR_DIR:?}/examples/guess-the-sketch/matchmaker
   skaffold run --build-concurrency=0 --cache-artifacts=false
   ```
1. Switch from Imagen2 to Imagen1 (as Imagen2 only generates large, high quality images, using Imagen1 will make game play faster)
   ```
   kubectl scale -ngenai deployment/vertex-image-api-imagen-1 --replicas=1
   kubectl scale -ngenai deployment/vertex-image-api-imagen-2 --replicas=0
   ```

To access the game, find the external IP for the frontend by running `kubectl get service -n genai guess-the-sketch-frontend` and open it in your browser.

### Troubleshooting

1. Check that you have ready GameServers
   ```
   kubectl get gs
   ```
1. Check that your frontend, matchmaker, and director are running:
   ```
   kubectl get pods -n genai
   ```

### Securing the frontend

By default, the game frontend runs over http on an IP address exposed to the internet.
If you would like to secure the frontend, you can enable the Google Cloud Identity-Aware
Proxy (IAP).

1. Allocate a static IP
   ```
   gcloud compute addresses create guess-the-sketch-ip --ip-version=IPV4 --network-tier=PREMIUM --global
   ```
1. Decide what domain to serve the application on. If you don't have a domain name, you can use sslip.io or nip.io with the static IP address previously provisioned (e.g. `34.49.41.103.sslip.io`)
1. Create a managed certificate for the chosen domain name:
   ```
   DOMAIN=34.49.41.103.sslip.io
   cat <<EOF > managed-cert.yaml
   apiVersion: networking.gke.io/v1
   kind: ManagedCertificate
   metadata:
     name: guess-the-sketch
     namespace: genai
   spec:
     domains:
     - ${DOMAIN}
   EOF
   kubectl apply -f managed-cert.yaml
   ```
1. Create an ingress using the static IP and managed certificate:
   ```
   cat <<EOF > static-ingress.yaml
   apiVersion: networking.k8s.io/v1
   kind: Ingress
   metadata:
     name: guess-the-sketch
     namespace: genai
     annotations:
       kubernetes.io/ingress.global-static-ip-name: guess-the-sketch-ip
       networking.gke.io/managed-certificates: guess-the-sketch
       kubernetes.io/ingress.class: "gce"
   spec:
     defaultBackend:
       service:
         name: guess-the-sketch-frontend
         port:
           number: 80
   EOF
   kubectl apply -f static-ingress.yaml
   ```
1. Configure your [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent)
1. [Create credentials](https://console.cloud.google.com/apis/credentials) for an OAuth 2.0 Client ID and make note of the Client ID and Client Secret
1. Create a secret in the `genai` namespace in your cluster holding the OAuth Client ID and Client Secret:
   ```
   kubectl create secret generic guess-the-sketch-secret -n genai --from-literal=client_id=client_id_key \
       --from-literal=client_secret=client_secret_key
   ```
1. Create a backend config in your cluster using the OAuth 2.0 credentials:
   ```
   cat <<EOF > backend-config.yaml
   apiVersion: cloud.google.com/v1
   kind: BackendConfig
   metadata:
     name: guess-the-sketch
     namespace: genai
   spec:
     iap:
       enabled: true
       oauthclientCredentials:
         secretName: guess-the-sketch
   EOF
   kubectl apply -f backend-config.yaml
   ```
1. Enable IAP for the backend service `genai/guess-the-sketch-frontend` [in the cloud console](https://console.cloud.google.com/security/iap)
1. Follow the instructions for [Enabling IAP for GKE](https://cloud.google.com/iap/docs/enabling-kubernetes-howto#enabling_iap) to add authorized users
1. Change the service type for the `guess-the-sketch-frontend` service from `LoadBalancer` to `ClusterIP` so that the only way to reach the game is through IAP:
   ```
   kubectl edit service -n genai guess-the-sketch-frontend
   ```
