import os, asyncio, cohere
from dotenv import load_dotenv

# I load my environment and set up my async client
load_dotenv()
co = cohere.AsyncClientV2(api_key=os.getenv("COHERE_API_KEY"))

async def main():
    print("--- Cohere Terminal (Command A) ---")
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    while True:
        try:
            # I wait for my input and break if quit
            user_input = input("\nMe: ").strip()
            if user_input.lower() == 'quit': break
            if not user_input: continue

            messages.append({"role": "user", "content": user_input})
            print("\nCohere: ", end="", flush=True)
            bot_reply = ""
            
            # I stream responses from the current 2026 stable model: command-a-03-2025
            async for event in co.chat_stream(model="command-a-03-2025", messages=messages):
                if event and event.type == "content-delta":
                    content = event.delta.message.content.text
                    if content:
                        print(content, end="", flush=True)
                        bot_reply += content
            
            print()
            messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            print(f"\n[Cohere Error]: {e}"); break

if __name__ == "__main__":
    asyncio.run(main())
