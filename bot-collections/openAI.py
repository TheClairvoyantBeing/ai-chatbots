import os, asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

# I load my configuration and initialize the client
load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def main():
    print("--- OpenAI Terminal (GPT-4o) ---")
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    while True:
        try:
            # I wait for my input
            user_input = input("\nMe: ").strip()
            if user_input.lower() == 'quit': break
            if not user_input: continue

            messages.append({"role": "user", "content": user_input})
            print("\nOpenAI: ", end="", flush=True)
            bot_reply = ""
            
            # I stream the response tokens
            stream = await client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    bot_reply += content
            print()
            messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            print(f"\n[OpenAI Error]: {e}"); break

if __name__ == "__main__":
    asyncio.run(main())
