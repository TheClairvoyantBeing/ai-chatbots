import os, asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

# I load my configuration and set up my NVIDIA NIM client
load_dotenv()
client = AsyncOpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

async def main():
    print("--- NVIDIA Nemotron Terminal (Thinking Mode) ---")
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    while True:
        try:
            # I wait for my input
            user_input = input("\nMe: ").strip()
            if user_input.lower() == 'quit': break
            if not user_input: continue

            messages.append({"role": "user", "content": user_input})
            print("\nNemotron: ", end="", flush=True)
            bot_reply = ""
            
            # I stream a response with reasoning traces enabled
            stream = await client.chat.completions.create(
                model="nvidia/nemotron-3-nano-30b-a3b",
                messages=messages,
                max_tokens=8192,
                stream=True,
                extra_body={
                    "reasoning_budget": 16384,
                    "chat_template_kwargs": {"enable_thinking": True}
                }
            )
            
            async for chunk in stream:
                if not chunk.choices: continue
                
                # I extract and print the 'thinking' part in grey
                reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
                if reasoning:
                    print(f"\033[90m{reasoning}\033[0m", end="", flush=True)
                
                # I print the actual response
                content = chunk.choices[0].delta.content
                if content:
                    print(content, end="", flush=True)
                    bot_reply += content
                    
            print() 
            messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            print(f"\n[NVIDIA Error]: {e}"); break

if __name__ == "__main__":
    asyncio.run(main())
