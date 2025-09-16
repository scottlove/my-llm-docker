# My LLM Docker

A containerized implementation of DavidAU's Mistral MOE model using Docker and AWS CodeBuild.

## Model
- **Model**: DavidAU/Mistral-MOE-4X7B-Dark-MultiVerse-Uncensored-Enhanced32-24B-gguf
- **Quantization**: Q4_K_M (14.7 GB)
- **Framework**: llama-cpp-python

## Build Process
This project uses AWS CodeBuild to:
1. Download the model from Hugging Face
2. Build a Docker image with the model
3. Push to Amazon ECR

## Local Testing
```bash
# Build locally (without model download)
docker build -t my-llm-docker .

# Run (you'd need to download model manually for local testing)
docker run -it my-llm-docker