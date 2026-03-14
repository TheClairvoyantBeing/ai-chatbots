#=======================================
# Use : pip install groq python-dotenv
#======================================

import os
import asyncio
from groq import AsyncGroq
from dotenv import load_dotenv

# I load my environment variables from the .env file
load_dotenv()

user_prompt = input("Prompt: ")
system_prompt = "Limit your answer to one sentence. Pretend you're a cat."

# I initialize my async client
client = AsyncGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

async def main():
    print("Chatbot started! Type 'quit' to exit.")
    
    # I store my conversation history
    messages = [
        {"role": "system", "content": system_prompt}
    ]

    while True:
        # I get my input inside the loop
        user_prompt = input("\nPrompt ('quit' to exit): ")
        
        # I check for the quit command BEFORE sending to my API
        if user_prompt.lower() == 'quit':
            print("Goodbye!")
            break
            
        # I add my message to the history
        messages.append({"role": "user", "content": user_prompt})

        # I send my entire list of messages to the model
        chat_completion = await client.chat.completions.create(
            messages=messages,
            model="llama-3.1-8b-instant", # I updated to a valid Groq model
        )

        response_text = chat_completion.choices[0].message.content
        print(f"\nCat: {response_text}")
        
        # I add the bot's response to my history so it remembers the conversation
        messages.append({"role": "assistant", "content": response_text})

if __name__ == "__main__":
    asyncio.run(main())