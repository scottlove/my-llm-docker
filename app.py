from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llama_cpp import Llama
import os
import uvicorn
from huggingface_hub import hf_hub_download

# Request/Response models


class ChatRequest(BaseModel):
    message: str
    max_tokens: int = 150
    temperature: float = 0.7


class ChatResponse(BaseModel):
    response: str
    tokens_used: int


# Initialize FastAPI
app = FastAPI(title="My LLM API", description="API for DavidAU Mistral model")

# Global model variable
llm = None


@app.on_event("startup")
async def load_model():
    global llm
    model_dir = "/app/models"
    model_filename = "M-MOE-4X7B-Dark-MultiVerse-UC-E32-24B-D_AU-Q2_k.gguf"
    model_path = f"{model_dir}/{model_filename}"

    # Create models directory
    os.makedirs(model_dir, exist_ok=True)

    # Download model if it doesn't exist
    if not os.path.exists(model_path):
        print("Model not found, downloading from Hugging Face...")
        try:
            hf_hub_download(
                repo_id="DavidAU/Mistral-MOE-4X7B-Dark-MultiVerse-Uncensored-Enhanced32-24B-gguf",
                filename=model_filename,
                local_dir=model_dir,
                local_dir_use_symlinks=False
            )
            print("Model download complete!")
        except Exception as e:
            print(f"Error downloading model: {e}")
            raise
    else:
        print("Model already exists, skipping download")

    print("Loading LLM model...")
    try:
        llm = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=4,
            n_gpu_layers=-1,  # Use all available GPU layers
            verbose=False
        )
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise


@app.get("/")
async def root():
    return {"message": "LLM API is running", "model": "DavidAU Mistral MOE 4x7B"}


@app.get("/health")
async def health_check():
    if llm is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy", "model_loaded": True}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if llm is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        response = llm(
            request.message,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=0.9,
            repeat_penalty=1.1,
            stop=[],
            echo=False
        )

        generated_text = response['choices'][0]['text']

        return ChatResponse(
            response=generated_text.strip(),
            tokens_used=response['usage']['total_tokens']
        )
    except Exception as e:
        print(f"Generation error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error generating response: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
