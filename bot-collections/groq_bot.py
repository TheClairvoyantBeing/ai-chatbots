#=========================================================================================
# My Groq Speed-Terminal
# 
# I built this to leverage Groq's LPU performance via their Python SDK.
#=========================================================================================

import os
import asyncio
from groq import AsyncGroq
from dotenv import load_dotenv

# I load my configuration from the .env file
load_dotenv()

# I initialize my blazing-fast async Groq client
client = AsyncGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

async def main():
    print("--- My Groq Terminal (Llama-3.1-8b) ---")
    print("I can type 'quit' to exit.")
    
    # I keep a local history of our chat so the model knows what we're talking about
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant. Provide concise and accurate answers."}
    ]

    while True:
        try:
            # I wait for my input
            user_prompt = input("\nMe: ").strip()
            
            if user_prompt.lower() == 'quit':
                print("Closing my Groq terminal. Goodbye!")
                break
                
            if not user_prompt:
                continue
                
            # I add my prompt to the session history
            messages.append({"role": "user", "content": user_prompt})

            print("\nGroq: ", end="", flush=True)
            full_response = ""

            # I stream the completion directly from the Groq API
            chat_completion = await client.chat.completions.create(
                messages=messages,
                model="llama-3.1-8b-instant",
                stream=True
            )

            # I collect and print the chunks as they arrive
            async for chunk in chat_completion:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_response += content

            print()
            
            # I record the bot's full response in the context
            messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            # I catch rate limits or API hiccups here
            print(f"\n[Trouble from Groq]: {e}")
            if "rate_limit" in str(e).lower():
                print("I might have hit my free-tier limit. I'll take a breather.")
            break

if __name__ == "__main__":
    # I start the event loop
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"My Groq script encountered a fatal error: {e}")