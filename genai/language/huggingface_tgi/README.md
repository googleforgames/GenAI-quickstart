## HuggingFace Text Generation Inference

Simple deployment of the [HuggingFace Text Generation Inference](https://huggingface.co/docs/text-generation-inference/en/index) 
(TGI) server running on GPUs.

You will need a GPU node pool to run this, for example:
```
gcloud container node-pools create gpu-l4x2-ssd --cluster genai-quickstart   --accelerator type=nvidia-l4,count=2,gpu-driver-version=latest   --machine-type g2-standard-24   --enable-image-streaming  --num-nodes=1 --min-nodes=1 --max-nodes=2  --zone us-west1-b --ephemeral-storage-local-ssd=count=2
```

To deploy:
```
# Set CUR_DIR to the top level directory of the git repo
export CUR_DIR=$(pwd)

cd genai/language/huggingface_tgi
skaffold run
```

To test:
```
kubectl port-forward -n genai svc/huggingface-tgi-api 8080:8080

# in appropriate virtualenv
cd $CURDIR
python3 genai/language/huggingface_tgi/example_api_call.py --endpoint http://localhost:8080/v1
```
