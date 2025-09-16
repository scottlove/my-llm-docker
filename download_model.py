#!/usr/bin/env python3

import os
from huggingface_hub import hf_hub_download

print("Starting model download...")

try:
    hf_hub_download(
        repo_id="DavidAU/Mistral-MOE-4X7B-Dark-MultiVerse-Uncensored-Enhanced32-24B-gguf",
        filename="M-MOE-4X7B-Dark-MultiVerse-UC-E32-24B-D_AU-Q4_k_m.gguf",
        local_dir="./models",
        local_dir_use_symlinks=False
    )
    print("Model download complete!")

    # Verify file exists
    model_path = "./models/M-MOE-4X7B-Dark-MultiVerse-UC-E32-24B-D_AU-Q4_k_m.gguf"
    if os.path.exists(model_path):
        size = os.path.getsize(model_path) / (1024**3)  # GB
        print(f"Model file exists: {size:.2f} GB")
    else:
        print("ERROR: Model file not found!")
        exit(1)

except Exception as e:
    print(f"Download error: {e}")
    exit(1)
