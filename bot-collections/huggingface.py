#=============================================
# My HuggingFace Chatbot
# Use : pip install huggingface_hub python-dotenv
#=============================================

import os
import asyncio
from huggingface_hub import AsyncInferenceClient
from dotenv import load_dotenv

# I load my environment variables
load_dotenv()

# I initialize my HuggingFace Async Client here
# I need to provide my HF_API_KEY in the .env file
client = AsyncInferenceClient(token=os.environ.get("HF_API_KEY"))

async def main():
    print("--- My HuggingFace Chatbot (Qwen/Qwen2.5-72B) ---")
    print("Type 'quit' to exit.")
    
    # I maintain my conversation history manually across the chat
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant powered by HuggingFace Hub."}
    ]

    while True:
        try:
            # I take my user input
            user_input = input("\nMe: ").strip()
            
            if user_input.lower() == 'quit':
                print("Shutting down my HuggingFace bot. Goodbye!")
                break
                
            if not user_input:
                continue

            # I append my message to my history
            messages.append({"role": "user", "content": user_input})
            
            print("\nHuggingFace: ", end="", flush=True)
            bot_reply = ""
            
            # I request a chat completion from an open-weight model on the Hub
            # I am using Qwen2.5-72B which is a massive state-of-the-art model
            response_stream = await client.chat_completion(
                model="Qwen/Qwen2.5-72B-Instruct",
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
                    
            print() 
            
            # I add the model's response back to my history
            messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            print(f"\n[API Error]: {e}")

if __name__ == "__main__":
    # I use clean async execution for my main loop
    asyncio.run(main())
