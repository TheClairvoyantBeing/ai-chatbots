#=============================================
# Use : pip install cohere python-dotenv
#=============================================

import os
import asyncio
import cohere
from dotenv import load_dotenv

load_dotenv()

# I initialize my Cohere Async Client here
# I need to provide my COHERE_API_KEY in the .env file
co = cohere.AsyncClientV2(api_key=os.environ.get("COHERE_API_KEY"))

async def main():
    print("Cohere Chatbot started! Type 'quit' to exit.")
    
    # I maintain my conversation history manually across the chat
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant powered by Cohere."}
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
            
            print("\nCohere: ", end="", flush=True)
            bot_reply = ""
            
            # I request a chat completion stream from the Cohere model
            # I am using the command-a-03-2025 model exactly as specified
            response_stream = co.chat_stream(
                model="command-a-03-2025", 
                messages=messages,
            )
            
            # I asynchronously iterate over the stream chunks
            async for event in response_stream:
                if event and event.type == "content-delta":
                    # Depending on the event structure, extract the text delta
                    if event.delta and event.delta.message and event.delta.message.content:
                        content = event.delta.message.content.text
                        if content:
                            print(content, end="", flush=True)
                            bot_reply += content
                    
            print() # Print a final newline when my stream is done
            
            # I add the model's response back to my history
            messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            print(f"\nAPI Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
