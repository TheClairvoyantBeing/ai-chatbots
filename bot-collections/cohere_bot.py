#=========================================================================================
# My Cohere Intelligent Terminal
# 
# I use this to interact with Cohere's Command-A models. I'm using their V2 API 
# for superior reasoning and coherent text generation.
#=========================================================================================

import os
import asyncio
import cohere
from dotenv import load_dotenv

# I load my environment variables
load_dotenv()

# I initialize my async Cohere client using the key from my .env
co = cohere.AsyncClientV2(api_key=os.environ.get("COHERE_API_KEY"))

async def main():
    print("--- My Cohere Terminal (command-a-03-2025) ---")
    print("I can type 'quit' to exit.")
    
    # I maintain my conversation history manually so the model stays on track
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant powered by Cohere."}
    ]

    while True:
        try:
            # I wait for my input
            user_input = input("\nMe: ").strip()
            
            if user_input.lower() == 'quit':
                print("Closing my Cohere terminal. Goodbye!")
                break
                
            if not user_input:
                continue

            # I add my message to the ongoing session history
            messages.append({"role": "user", "content": user_input})
            
            print("\nCohere: ", end="", flush=True)
            bot_reply = ""
            
            # I request a chat completion stream from the high-performance Command-A model
            response_stream = co.chat_stream(
                model="command-a-03-2025", 
                messages=messages,
            )
            
            # I wrap my async iteration in a try-block to catch streaming hiccups
            async for event in response_stream:
                if event and event.type == "content-delta":
                    if event.delta and event.delta.message and event.delta.message.content:
                        content = event.delta.message.content.text
                        if content:
                            print(content, end="", flush=True)
                            bot_reply += content
                    
            print() # I add a final newline once my stream finishes
            
            # I record the bot's response in our history for context
            messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            # I catch API errors or connectivity issues here
            print(f"\n[Note from Cohere]: {e}")
            break

if __name__ == "__main__":
    # I fire up the main loop with a clean async runner
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"My Cohere terminal crashed: {e}")
