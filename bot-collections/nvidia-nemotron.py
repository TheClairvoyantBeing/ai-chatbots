#=========================================================================================
# My NVIDIA Nemotron Reasoning-Terminal
# 
# I use this to interact with NVIDIA's NIM API. This model is unique because it 
# displays its "Thinking" process (reasoning) before giving its final answer.
#=========================================================================================

import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

# I load my environment variables
load_dotenv()

# I initialize my OpenAI-compatible client pointing to NVIDIA's NIM API
client = AsyncOpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ.get("NVIDIA_API_KEY")
)

async def main():
    print("--- My NVIDIA Nemotron Terminal (Thinking Mode Enabled) ---")
    print("I can type 'quit' to exit.")
    
    # I maintain my conversation history manually to keep the context coherent
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant powered by NVIDIA Nemotron."}
    ]

    while True:
        try:
            # I wait for my input
            user_input = input("\nMe: ").strip()
            
            if user_input.lower() == 'quit':
                print("Closing my NVIDIA terminal. Goodbye!")
                break
                
            if not user_input:
                continue

            # I add my message to our ongoing session history
            messages.append({"role": "user", "content": user_input})
            
            print("\nNemotron: ", end="", flush=True)
            bot_reply = ""
            
            # I request a response with internal reasoning traces enabled.
            # I've given it a 'reasoning_budget' so it has plenty of room to think!
            response_stream = await client.chat.completions.create(
                model="nvidia/nemotron-3-nano-30b-a3b",
                messages=messages,
                temperature=1.0,
                top_p=1.0,
                max_tokens=8192,
                stream=True,
                extra_body={
                    "reasoning_budget": 16384,
                    "chat_template_kwargs": {"enable_thinking": True}
                }
            )
            
            # I asynchronously iterate over the incoming stream
            async for chunk in response_stream:
                if not chunk.choices:
                    continue
                
                # I extract the model's internal thinking process (reasoning)
                reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
                if reasoning:
                    # I print the reasoning in grey color so it's clearly separate from the answer
                    print(f"\033[90m{reasoning}\033[0m", end="", flush=True)
                
                # I extract the actual response content
                content = chunk.choices[0].delta.content
                if content is not None:
                    print(content, end="", flush=True)
                    bot_reply += content
                    
            print() 
            
            # I save the response back into our history for context
            messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            # I catch API errors or connectivity issues here
            print(f"\n[Note from NVIDIA NIM]: {e}")
            break

if __name__ == "__main__":
    # I start the async main loop
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"My NVIDIA terminal crashed with a fatal error: {e}")
