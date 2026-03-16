#=========================================================================================
# My OpenAI Chat Terminal
# 
# I use this to interact with GPT-4o via my CLI. 
# Requires: paid credits on my OpenAI account and a valid key in my .env.
#=========================================================================================

import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

# I pull in my environment variables (like my secret API key)
load_dotenv()

# I initialize my asynchronous OpenAI client
# I make sure to pull the key directly from my .env file
client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

async def main():
    print("--- My OpenAI Chat Terminal (GPT-4o) ---")
    print("I can type 'quit' to close this session.")
    
    # I start my session with a polite system prompt
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant. Always be polite and remarkably accurate."}
    ]

    while True:
        try:
            # I wait for my next command
            user_input = input("\nMe: ").strip()
            
            if user_input.lower() == 'quit':
                print("Closing my OpenAI terminal. Goodbye!")
                break
                
            if not user_input:
                continue

            # I keep track of our conversation context here
            messages.append({"role": "user", "content": user_input})
            
            print("\nOpenAI: ", end="", flush=True)
            bot_reply = ""
            
            # I request a streaming response so I can see the AI "think" in real-time
            response_stream = await client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                stream=True
            )
            
            # I catch each chunk of text as it streams in
            async for chunk in response_stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    bot_reply += content
            
            print()
            
            # I save the bot's full thought to our history
            messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            # If I hit a quota limit or my key is wrong, I'll catch that here
            print(f"\n[Note from my system]: {e}")
            if "insufficient_quota" in str(e).lower():
                print("I probably need to add some credits to my OpenAI account to keep going.")
            break

if __name__ == "__main__":
    # I fire up the main loop using a clean async runner
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"My terminal crashed with a fatal error: {e}")