#=============================================
# My NVIDIA Nemotron Chatbot
# Use : pip install openai python-dotenv
#=============================================

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
    print("--- My NVIDIA Nemotron Chatbot (Reasoning Enabled) ---")
    print("Type 'quit' to exit.")
    
    # I maintain my conversation history manually
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant powered by NVIDIA Nemotron."}
    ]

    while True:
        try:
            # I take my user input
            user_input = input("\nMe: ").strip()
            
            if user_input.lower() == 'quit':
                print("Shutting down my NVIDIA bot. Goodbye!")
                break
                
            if not user_input:
                continue

            # I append my message to the history
            messages.append({"role": "user", "content": user_input})
            
            print("\nNemotron: ", end="", flush=True)
            bot_reply = ""
            
            # I request a response with internal reasoning traces enabled
            # Note: I am providing a 'reasoning_budget' so the model can "think" before it speaks
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
                    # I print my reasoning in a grey color to distinguish it from the final answer
                    print(f"\033[90m{reasoning}\033[0m", end="", flush=True)
                
                # I extract my actual response content
                content = chunk.choices[0].delta.content
                if content is not None:
                    print(content, end="", flush=True)
                    bot_reply += content
                    
            print() 
            
            # I add the model's response back to my history
            messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            print(f"\n[API Error]: {e}")

if __name__ == "__main__":
    # I use clean async execution
    asyncio.run(main())
