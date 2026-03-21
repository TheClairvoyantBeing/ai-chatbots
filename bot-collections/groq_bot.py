import os, asyncio
from groq import AsyncGroq
from dotenv import load_dotenv

# I load my configuration and initialize Groq
load_dotenv()
client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

async def main():
    print("--- Groq Terminal (Llama-3.1-8b) ---")
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    while True:
        try:
            # I wait for my input
            user_input = input("\nMe: ").strip()
            if user_input.lower() == 'quit': break
            if not user_input: continue
                
            messages.append({"role": "user", "content": user_input})
            print("\nGroq: ", end="", flush=True)
            bot_reply = ""

            # I stream the completion directly from Groq
            stream = await client.chat.completions.create(
                messages=messages,
                model="llama-3.1-8b-instant",
                stream=True
            )

            async for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    print(content, end="", flush=True)
                    bot_reply += content

            print()
            messages.append({"role": "assistant", "content": bot_reply})

        except Exception as e:
            print(f"\n[Groq Error]: {e}"); break

if __name__ == "__main__":
    asyncio.run(main())