#=========================================================================================
# My HuggingFace Inference Terminal
# 
# I use this to reach out to open-source giants like Qwen-2.5-72B directly 
# on the HuggingFace Hub via their serverless inference API.
#=========================================================================================

import os
import asyncio
from huggingface_hub import AsyncInferenceClient
from dotenv import load_dotenv

# I load my configuration from the .env file
load_dotenv()

# I initialize my HuggingFace Async Client using my personal access token
client = AsyncInferenceClient(token=os.environ.get("HF_API_KEY"))

async def main():
    print("--- My HuggingFace Terminal (Qwen-2.5-72B) ---")
    print("I can type 'quit' to exit.")
    
    # I maintain my conversation history manually to keep the chat coherent
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant powered by HuggingFace Hub."}
    ]

    while True:
        try:
            # I wait for my input
            user_input = input("\nMe: ").strip()
            
            if user_input.lower() == 'quit':
                print("Closing my HuggingFace terminal. Goodbye!")
                break
                
            if not user_input:
                continue

            # I add my message to our ongoing session history
            messages.append({"role": "user", "content": user_input})
            
            print("\nHuggingFace: ", end="", flush=True)
            bot_reply = ""
            
            # I request a streaming completion from a massive 72B parameter model
            response_stream = await client.chat_completion(
                model="Qwen/Qwen2.5-72B-Instruct",
                messages=messages,
                max_tokens=2048,
                stream=True,
            )
            
            # I asynchronously iterate over the chunks as they stream in
            async for chunk in response_stream:
                content = chunk.choices[0].delta.content
                if content is not None:
                    print(content, end="", flush=True)
                    bot_reply += content
                    
            print() 
            
            # I save the response back into my history for context
            messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            # I catch API timeouts or model loading errors here
            print(f"\n[Note from HuggingFace]: {e}")
            if "loading" in str(e).lower():
                print("The model is still loading on the server. I should try again in a minute.")
            break

if __name__ == "__main__":
    # I run the async main loop
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"My HuggingFace terminal crashed: {e}")
