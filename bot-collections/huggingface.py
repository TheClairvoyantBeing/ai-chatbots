#=============================================
# Use : pip install huggingface_hub python-dotenv
#=============================================

import os
import asyncio
from huggingface_hub import AsyncInferenceClient
from dotenv import load_dotenv

load_dotenv()

# I initialize my HuggingFace Async Client here
# I need to provide my HF_API_KEY in the .env file
client = AsyncInferenceClient(token=os.environ.get("HF_API_KEY"))

async def main():
    print("HuggingFace Chatbot started! Type 'quit' to exit.")
    
    # I maintain my conversation history manually across the chat
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant powered by HuggingFace."}
    ]

    while True:
        try:
            user_input = input("\nPrompt ('quit' to exit): ")
            
            if user_input.strip().lower() == 'quit':
                print("Goodbye!")
                break
                
            if not user_input.strip():
                continue

            # I append my message to the history
            messages.append({"role": "user", "content": user_input})
            
            print("\nHuggingFace: ", end="", flush=True)
            bot_reply = ""
            
            # I request a chat completion from an open-weight model on the Hub
            # I can change this to any model ID on huggingface.co that supports Chat Completions!
            response_stream = await client.chat_completion(
                model="Qwen/Qwen2.5-72B-Instruct", # Massive state-of-the-art model fully supported on the free tier
                messages=messages,
                max_tokens=2048,
                stream=True,
            )
            
            # I asynchronously iterate over the stream chunks
            async for chunk in response_stream:
                content = chunk.choices[0].delta.content
                if content is not None:
                    print(content, end="", flush=True)
                    bot_reply += content
                    
            print() # Print a final newline when my stream is done
            
            # I add the model's response back to my history
            messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            print(f"\nAPI Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
