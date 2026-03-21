import os, asyncio, sys, json, httpx
from dotenv import load_dotenv
from google import genai
import cohere
from groq import AsyncGroq
from openai import AsyncOpenAI
from huggingface_hub import AsyncInferenceClient

load_dotenv()

# I set up my specialized clients for each provider
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
cohere_client = cohere.AsyncClientV2(api_key=os.getenv("COHERE_API_KEY"))
groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
hf_client = AsyncInferenceClient(token=os.getenv("HF_API_KEY"))
nvidia_client = AsyncOpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=os.getenv("NVIDIA_API_KEY"))

async def stream_council_member(name, full_prompt, color_code, silent=False):
    """I manage the streaming response for each council member."""
    if not silent: print(f"\n{color_code}=== [ {name} is taking the floor... ] ===\033[0m")
    response_text = ""
    try:
        # I select the right model and stream based on the provider
        if name == "Gemini (Google)":
            async for chunk in await gemini_client.aio.models.generate_content_stream(model='gemini-2.5-flash-lite', contents=full_prompt):
                if chunk.text:
                    if not silent: print(f"{color_code}{chunk.text}\033[0m", end="", flush=True)
                    response_text += chunk.text
                    
        elif name == "Cohere (Command-A)":
            # Updated to the specific 2026 stable model: command-a-03-2025
            async for event in cohere_client.chat_stream(model="command-a-03-2025", messages=[{"role": "user", "content": full_prompt}]):
                if event and event.type == "content-delta":
                    content = event.delta.message.content.text
                    if content:
                        if not silent: print(f"{color_code}{content}\033[0m", end="", flush=True)
                        response_text += content
                        
        elif name.startswith("Groq"):
            stream = await groq_client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": full_prompt}], stream=True)
            async for chunk in stream:
                if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    if not silent: print(f"{color_code}{content}\033[0m", end="", flush=True)
                    response_text += content
                    
        elif name == "NVIDIA (Nemotron)":
            stream = await nvidia_client.chat.completions.create(model="nvidia/nemotron-3-nano-30b-a3b", messages=[{"role": "user", "content": full_prompt}], stream=True, extra_body={"reasoning_budget": 16384})
            async for chunk in stream:
                if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    if not silent: print(f"{color_code}{content}\033[0m", end="", flush=True)
                    response_text += content
                    
        elif name == "OpenAI (GPT-4o)":
            stream = await openai_client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": full_prompt}], stream=True, max_tokens=600)
            async for chunk in stream:
                if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    if not silent: print(f"{color_code}{content}\033[0m", end="", flush=True)
                    response_text += content
                    
        elif name == "HuggingFace (Qwen)":
            # Wrapped in a sub-try block to handle the HF library bug gracefully
            try:
                async for chunk in await hf_client.chat_completion(model="Qwen/Qwen2.5-72B-Instruct", messages=[{"role": "user", "content": full_prompt}], max_tokens=600, stream=True):
                    if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        if not silent: print(f"{color_code}{content}\033[0m", end="", flush=True)
                        response_text += content
            except (IndexError, StopAsyncIteration):
                pass
                    
        elif name == "Ollama (Local)":
            async with httpx.AsyncClient() as client:
                async with client.stream("POST", "http://localhost:11434/api/chat", json={"model": "llama3.1", "messages": [{"role": "user", "content": "hi"}], "stream": True}, timeout=None) as response:
                    async for line in response.aiter_lines():
                        if line:
                            content = json.loads(line).get("message", {}).get("content", "")
                            if content:
                                if not silent: print(f"{color_code}{content}\033[0m", end="", flush=True)
                                response_text += content
                                
    except Exception as e:
        if not silent: print(f"{color_code}[Note: {name} failed: {e}]\033[0m")
        return None
        
    if not silent: print()
    return f"\n--- {name} ---\n{response_text}\n"

async def simulate_thinking(seconds=5):
    """I provide a simple progress indicator duringcouncil deliberation."""
    print("\n\033[33m[ My council is deliberating intensely... ]\033[0m")
    chars = "/—\\"
    for i in range(seconds * 5):
        sys.stdout.write(f"\r  {chars[i%3]} Thinking and sharing thoughts internally...")
        sys.stdout.flush()
        await asyncio.sleep(0.2)
    sys.stdout.write("\r  Done! Synthesis complete. Final verdict incoming...\n")

async def main():
    print("--- Welcome to the AI Debate Council ---")
    council = [
        ("NVIDIA (Nemotron)", "\033[38;5;208m"), ("Gemini (Google)", "\033[94m"),
        ("Cohere (Command-A)", "\033[92m"), ("Groq (Llama-3.1)", "\033[95m"),
        ("Ollama (Local)", "\033[96m"), ("OpenAI (GPT-4o)", "\033[93m"),
        ("HuggingFace (Qwen)", "\033[91m")
    ]
    
    while True:
        try:
            user_input = input("\nTopic for Debate ('quit' to exit): ").strip()
            if user_input.lower() == 'quit': break
            if not user_input: continue

            # Phase 1: Opening Remarks (Silent)
            opening_remarks = []
            for name, color in council:
                remark = await stream_council_member(name, f"Give your brief opening statement about '{user_input}'. Max 500 words.", color, silent=True)
                if remark: opening_remarks.append(remark)
            
            if not opening_remarks: continue
            transcript = "".join(opening_remarks)

            # Phase 2: Cross-Examination (Silent)
            critiques = []
            for name, color in council:
                critique = await stream_council_member(name, f"Topic: '{user_input}'. Peer remarks: {transcript}. Critique them briefly.", color, silent=True)
                if critique: critiques.append(critique)

            await simulate_thinking(10)

            # Phase 3: The Verdict (Public)
            print(f"\n[ THE FINAL VERDICT: 5-BULLET SUMMARIES ]")
            for name, color in council:
                await stream_council_member(name, f"Topic: '{user_input}'. Final verdict in EXACTLY 5 BULLET POINTS.", color, silent=False)
                
        except Exception as e:
            print(f"\n[Error]: {e}")

if __name__ == "__main__":
    if os.name == 'nt': asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
