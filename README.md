# LLMCondense - A Simple LLM Document Summarizer
## Short description

Simple document summarization webapp using the power of LLMs. This will include:
- LLM deployment using [HuggingFace Text Generation Inference](https://github.com/huggingface/text-generation-inference);
- [Streamlit](https://streamlit.io/) for the WebApp interface (UI);
- [LangChain](https://python.langchain.com/docs/get_started/introduction.html) as the backend framework.

This repo can be used as base for other applications that use LLMs.

## Pre-requisites

`Ubuntu` or `Windows` with the following installed:
- [Miniconda3](https://docs.conda.io/en/latest/miniconda.html) 
- [Docker](https://docs.docker.com/engine/install/ubuntu/)
- [Docker Compose](https://docs.docker.com/compose/install/linux/)

You could use `WSL2` on a `Windows` machine, as an alternative to an `Ubuntu` machine.

## Setup your machine (local or remote server)
### 1. Serve your LLM using HuggingFace 🤗 - *Text Generation Inference*
**Text Generation Inference** is a Rust, Python, and gRPC server designed for text generation inference, featuring optimized architectures, tensor parallelism, and production-ready capabilities. This is used by HuggingFace for various services. For more info, visit the [official GitHub repo](https://github.com/huggingface/text-generation-inference).

Very quickly:
- Clone this repo and navigate inside it:
```bash
git clone https://github.com/pandego/LLMCondense.git
cd LLMCondence
```

- Create your environment and install the necessary libraries in it using the `requirements.txt` file:
```bash
conda create -n llmcondense python=3.11.4
conda activate llmcondense
pip install -r requirements.txt
```

- Define a shared volume, where your LLM will be downloaded to. This will avoid downloading weights on every run:
```bash
volume=$PWD/data # share a volume with the Docker container to avoid downloading weights every run
```

- Chose the LLM you will be working with. 
```bash
model=tiiuae/falcon-7b-instruct
```
- If you are thinking of using a model like `llama2`, you will need to include a HuggingFace `token` too:
```bash
token=hf_your_token_here
```

- Run the following command to build and run your container, where your model will be downloaded and served:
```bash
docker run --gpus all --shm-size 1g -e HUGGING_FACE_HUB_TOKEN=$token -p 8080:80 -v $volume:/data ghcr.io/huggingface/text-generation-inference:1.0.3 --model-id $model
```

***Note 1***: If you want to use more then one GPU, you can add `-e CUDA_VISIBLE_DEVICES=0,1` in order to shard the model on 2 processes.

***Note 2***: You can add `-e NCCL_P2P_DISABLE=1` in case you get "`Some NCCL operations have failed or timed out`" error while loading the model - described in [Issue 654](https://github.com/huggingface/text-generation-inference/issues/654) of the *Text Generation Inference* repo.

***Note 3***: You can decrease the `--max-batch-prefill-tokens` in order to decrease memory needs.

- For example:
```bash
docker run --gpus all --shm-size 1g -e CUDA_VISIBLE_DEVICES=0,1 -e NCCL_P2P_DISABLE=1 -e HUGGING_FACE_HUB_TOKEN=$token -p 8080:80 -v $volume:/data ghcr.io/huggingface/text-generation-inference:1.0.3 --model-id $model --max-batch-prefill-tokens 2048
```


And that's it, your LLM should be served!

### 2. Test your served LLM 
- To test it you can simply navigate to http://127.0.0.1:8080/docs and "*Try it out*" using one of the two methods - `/generate` or `/generate_stream`:
    - `/generate` will output the response in a "*one-shot*" fashion.
    - `/generate_stream` will output the response in a "*word-by-word*" fashion.
- Alternatively you can send a `-POST` *request* and checkout the server's *response* for each method:
```bash
# /generate 
curl 127.0.0.1:8080/generate \
    -X POST \
    -d '{"inputs":"What is Deep Learning?","parameters":{"max_new_tokens":20}}' \
    -H 'Content-Type: application/json'

# /generate_stream
curl 127.0.0.1:8080/generate_stream \
    -X POST \
    -d '{"inputs":"What is Deep Learning?","parameters":{"max_new_tokens":20}}' \
    -H 'Content-Type: application/json'
```

### 3. Launch the Streamlit App
- This part is straighforward as well, simply run the next command from your terminal:
```bash
streamlit run main.py
```
- Navigate to the *Streamlit WebApp* at http://localhost:8501.


That's it! 🥳 You can now start using LLM Condense to summarize your texts!

## TODOs
- Include LangChain framework for:
    - Prompt templating
    - Document loading
    - Chain handling
- Docker Compose
___
🎊 ***Et voilà!*** 🎊

## References:
- https://docs.streamlit.io/
- https://docs.langchain.com/docs/
- https://github.com/huggingface/text-generation-inference/