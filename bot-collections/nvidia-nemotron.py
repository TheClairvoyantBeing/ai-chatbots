#=============================================
# Use : pip install openai python-dotenv
#=============================================

import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

# I initialize my OpenAI client pointing to the NVIDIA API endpoint
client = AsyncOpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ.get("NVIDIA_API_KEY")
)

async def main():
    print("NVIDIA Nemotron Chatbot started! Type 'quit' to exit.")
    
    # I maintain my conversation history manually since my API evaluates the whole chat
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant powered by NVIDIA Nemotron."}
    ]

    while True:
        try:
            user_input = input("\nPrompt ('quit' to exit): ")
            
            if user_input.strip().lower() == 'quit':
                print("Goodbye!")
                break
                
            if not user_input.strip():
                continue

            # I append my message to the history
            messages.append({"role": "user", "content": user_input})
            
            # I request a response from the NVIDIA Nemotron model with streaming and reasoning enabled
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
            
            print("\nNemotron: ", end="", flush=True)
            bot_reply = ""
            
            # I asynchronously iterate over my stream
            async for chunk in response_stream:
                if not chunk.choices:
                    continue
                
                # I try to extract my reasoning traces (if the model provides its internal thought process)
                reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
                if reasoning:
                    print(f"\033[90m{reasoning}\033[0m", end="", flush=True) # Print reasoning in grey color (optional)
                
                # I extract my actual content
                content = chunk.choices[0].delta.content
                if content is not None:
                    print(content, end="", flush=True)
                    bot_reply += content
                    
            print() # I print a final newline when my stream is done
            
            # I add the model's response back to my history
            messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            print(f"\nAPI Error: {e}")

if __name__ == "__main__":
    # I ensure my asyncio event loop handles the async bot correctly
    asyncio.run(main())
