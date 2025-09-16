from llama_cpp import Llama
import os

# Initialize the model
model_path = "/app/models/M-MOE-4X7B-Dark-MultiVerse-UC-E32-24B-D_AU-Q4_k_m.gguf"

print("Loading model...")
llm = Llama(
    model_path=model_path,
    n_ctx=2048,  # Context length
    n_threads=4,  # Number of threads
    verbose=False
)
print("Model loaded successfully!")

# Simple test
prompt = "Hello, how are you today?"
print(f"Prompt: {prompt}")

response = llm(
    prompt,
    max_tokens=100,
    temperature=0.7,
    stop=["</s>"]
)

print(f"Response: {response['choices'][0]['text']}")
print("LLM is working correctly!")
