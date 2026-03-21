import os, asyncio
from huggingface_hub import AsyncInferenceClient
from dotenv import load_dotenv

# I load my configuration and initialize HF
load_dotenv()
client = AsyncInferenceClient(token=os.getenv("HF_API_KEY"))

async def main():
    print("--- HuggingFace Terminal (Qwen-2.5-72B) ---")
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    while True:
        try:
            # I wait for my input
            user_input = input("\nMe: ").strip()
            if user_input.lower() == 'quit': break
            if not user_input: continue

            messages.append({"role": "user", "content": user_input})
            print("\nHuggingFace: ", end="", flush=True)
            bot_reply = ""
            
            # I stream the completion from a massive 72B model
            stream = await client.chat_completion(
                model="Qwen/Qwen2.5-72B-Instruct",
                messages=messages,
                max_tokens=2048,
                stream=True,
            )
            
            # I wrap the async iteration in a more robust way to handle the HF streaming library bug
            try:
                async for chunk in stream:
                    if chunk.choices and len(chunk.choices) > 0:
                        content = chunk.choices[0].delta.content
                        if content:
                            print(content, end="", flush=True)
                            bot_reply += content
            except (IndexError, StopAsyncIteration):
                # This catches the known library issue with the [DONE]\n token at the end of stream
                pass
            except Exception as stream_err:
                print(f"[Note: Stream interrupted: {stream_err}]")
                
            print()
            messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            print(f"\n[HF Error]: {e}"); break

if __name__ == "__main__":
    asyncio.run(main())
