from llama_cpp import Llama
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llama_cpp import Llama
import os
import uvicorn

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
    model_path = "/app/models/M-MOE-4X7B-Dark-MultiVerse-UC-E32-24B-D_AU-Q4_k_m.gguf"

    print("Loading LLM model...")
    try:
        llm = Llama(
            model_path=model_path,
            n_ctx=2048,  # Context length
            n_threads=4,  # Adjust based on your container resources
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
            stop=["</s>", "\n\n"]  # Stop sequences
        )

        return ChatResponse(
            response=response['choices'][0]['text'].strip(),
            tokens_used=response['usage']['total_tokens']
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating response: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
