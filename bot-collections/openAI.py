#=========================================================
# My OpenAI Chatbot
# Use: pip install openai python-dotenv
# To run this: python bot-collections/openAI.py
# 
# NOTE: I cannot execute this script currently because my 
# OpenAI account requires paid credits.
#=========================================================

import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

# I automatically load my environment variables from my .env file
load_dotenv()

# I initialize my asynchronous OpenAI client
client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

async def main():
    print("--- My OpenAI Chatbot (GPT-4o) ---")
    print("Type 'quit' to exit.")
    
    # I maintain my conversation history
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant. Always be polite and remarkably accurate."}
    ]

    while True:
        try:
            # I take my user input
            user_input = input("\nMe: ").strip()
            
            if user_input.lower() == 'quit':
                print("Shutting down my OpenAI bot. Goodbye!")
                break
                
            if not user_input:
                continue

            # I append my message to my history
            messages.append({"role": "user", "content": user_input})
            
            print("\nOpenAI: ", end="", flush=True)
            bot_reply = ""
            
            # I request a streaming chat completion from the GPT-4o model
            response_stream = await client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                stream=True
            )
            
            # I iterate through my incoming chunks
            async for chunk in response_stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    bot_reply += content
            
            print()
            
            # I add the bot's response to my history context
            messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            # If I don't have credits, I'll catch the error here
            print(f"\n[Error]: {e}")
            if "insufficient_quota" in str(e).lower():
                print("Note: I need to add credits to my OpenAI account to use this script.")
            break

if __name__ == "__main__":
    # I use clean async execution
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Fatal error: {e}")