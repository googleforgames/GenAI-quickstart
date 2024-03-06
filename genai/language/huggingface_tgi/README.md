## HuggingFace Text Generation Inference

Simple deployment of the [HuggingFace Text Generation Inference](https://huggingface.co/docs/text-generation-inference/en/index)
(TGI) server running on GPUs.

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
