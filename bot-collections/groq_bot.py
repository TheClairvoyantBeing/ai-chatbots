#=============================================
# My Groq Chatbot
# Use : pip install groq python-dotenv
#=============================================

import os
import asyncio
from groq import AsyncGroq
from dotenv import load_dotenv

# I load my environment variables from the .env file
load_dotenv()

# I initialize my async Groq client
client = AsyncGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

async def main():
    print("--- My Groq Chatbot (llama-3.1-8b-instant) ---")
    print("Type 'quit' to exit.")
    
    # I store my conversation history locally
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant. Provide concise and accurate answers."}
    ]

    while True:
        try:
            # I take my user input
            user_prompt = input("\nMe: ").strip()
            
            if user_prompt.lower() == 'quit':
                print("Shutting down my Groq bot. Goodbye!")
                break
                
            if not user_prompt:
                continue
                
            # I add my message to my history
            messages.append({"role": "user", "content": user_prompt})

            print("\nGroq: ", end="", flush=True)
            full_response = ""

            # I send my entire conversation history to the model with streaming enabled
            chat_completion = await client.chat.completions.create(
                messages=messages,
                model="llama-3.1-8b-instant",
                stream=True
            )

            async for chunk in chat_completion:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_response += content

            print()
            
            # I add the bot's response to my history so it remembers the context
            messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            print(f"\n[API Error]: {e}")

if __name__ == "__main__":
    # I use clean async execution
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Fatal error: {e}")