# =========================================================================================
# Why I am using this script (test_hf.py):
# 
# HuggingFace frequently rotates which models are active on their free-tier 
# Serverless Inference API. A model that works today might return a 
# "model_not_supported" error tomorrow if they remove it from the free rotation.
#
# I created this diagnostic script to automatically test an array of popular 
# open-source models against my specific HF_API_KEY. This script will iterate 
# through the list and instantly tell me which model is currently live and 
# available for free chat completion streaming. Once it finds a working model,
# I can copy that model ID and paste it back into my main `bot-collections\huggingface.py` bot!
# =========================================================================================

import asyncio
import os
from huggingface_hub import AsyncInferenceClient
from dotenv import load_dotenv

# I load my environment variables
load_dotenv()

async def list_models():
    # I initialize my client with my HuggingFace API token
    client = AsyncInferenceClient(token=os.environ.get('HF_API_KEY'))
    
    # I define a list of powerful models I want to check
    models = [
        "Qwen/Qwen2.5-72B-Instruct",
        "meta-llama/Meta-Llama-3-8B-Instruct",
        "mistralai/Mistral-7B-Instruct-v0.2",
        "HuggingFaceH4/zephyr-7b-beta",
        "google/gemma-2-9b-it",
        "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "google/gemma-7b-it",
        "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO"
    ]
    
    print("--- Starting my HuggingFace Diagnostic Test ---")
    
    # I iterate through each model to see which one works
    for m in models:
        try:
            print(f"Testing {m}...")
            
            # I send a simple "hi" prompt as a ping test
            response = await client.chat_completion(
                model=m, 
                messages=[{'role': 'user', 'content': 'hi'}], 
                max_tokens=10
            )
            # If my request succeeds, I print the success message and stop looking
            print(f"  -> SUCCESS! I found a working free-tier model: {m}")
            return
        except Exception as e:
            # If the model is not supported or errors out, I catch it and try the next one
            print(f"  -> FAILED: {e}")
            
    print("\n[I could not find any working models in my current list!]")

# I run my async diagnostic test
if __name__ == "__main__":
    asyncio.run(list_models())
