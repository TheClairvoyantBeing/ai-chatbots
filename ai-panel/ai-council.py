#=========================================================================================
# My Elite AI Council - A 3-Stage Formal Debate Terminal
# 
# I built this to let the world's most powerful models battle it out over any topic.
#
# Process:
# Stage 1: My council members generate independent opening statements in private.
# Stage 2: They cross-examine each other, critiquing flaws and defending their logic.
# Stage 3: The final verdict—a concise, fact-checked summary in 5 sharp bullets.
#
# Constraints: I've tuned this to keep responses under 500 words per member.
#
# Local Setup (Ollama):
# 1. I download Ollama from https://ollama.com/
# 2. I pull the model: ollama pull llama3.1
# 3. I fire up the server and run this council!
#=========================================================================================

import os
import asyncio
import time
import sys
import json
import httpx
from dotenv import load_dotenv

# I pull in the heavy hitters—OpenAI, Google, Groq, Cohere, and Hugging Face
from google import genai
import cohere
from groq import AsyncGroq
from openai import AsyncOpenAI
from huggingface_hub import AsyncInferenceClient

# I load my secret API keys from the .env file
load_dotenv()

# I set up my specialized clients for each provider
gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
cohere_client = cohere.AsyncClientV2(api_key=os.environ.get("COHERE_API_KEY"))
groq_client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))
openai_client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
hf_client = AsyncInferenceClient(token=os.environ.get("HF_API_KEY"))

async def stream_council_member(name, full_prompt, color_code, silent=False):
    """I manage the streaming response for each council member, handling errors gracefully."""
    if not silent:
        print(f"\n{color_code}=== [ {name} is taking the floor... ] ===\033[0m")
    
    response_text = ""
    
    try:
        if name == "Gemini (Google)":
            response_stream = await gemini_client.aio.models.generate_content_stream(
                model='gemini-2.5-flash',
                contents=full_prompt
            )
            async for chunk in response_stream:
                if chunk.text:
                    if not silent:
                        print(f"{color_code}{chunk.text}\033[0m", end="", flush=True)
                    response_text += chunk.text
                    
        elif name == "Cohere (Command-R)":
            response_stream = cohere_client.chat_stream(
                model="command-a-03-2025", 
                messages=[{"role": "user", "content": full_prompt}]
            )
            async for event in response_stream:
                if event and event.type == "content-delta":
                    content = event.delta.message.content.text
                    if content:
                        if not silent:
                            print(f"{color_code}{content}\033[0m", end="", flush=True)
                        response_text += content
                        
        elif name.startswith("Groq"):
            # I use Llama-3.1 on Groq for that near-instant speed
            response_stream = await groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": full_prompt}],
                stream=True
            )
            async for chunk in response_stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    if not silent:
                        print(f"{color_code}{content}\033[0m", end="", flush=True)
                    response_text += content

        elif name == "NVIDIA (Nemotron)":
            # I use NVIDIA Nemotron for powerful reasoning without OpenAI credit issues
            response_stream = await client.chat.completions.create(
                model="nvidia/nemotron-3-nano-30b-a3b",
                messages=[{"role": "user", "content": full_prompt}],
                temperature=1.0,
                top_p=1.0,
                max_tokens=600,
                extra_body={"reasoning_budget": 16384},
                stream=True
            )
            async for chunk in response_stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    if not silent:
                        print(f"{color_code}{content}\033[0m", end="", flush=True)
                    response_text += content

        elif name == "OpenAI (GPT-4o)":
            # I've capped this at ~600 tokens to stay around my 500-word limit
            response_stream = await openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": full_prompt}],
                stream=True,
                max_tokens=600 
            )
            async for chunk in response_stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    if not silent:
                        print(f"{color_code}{content}\033[0m", end="", flush=True)
                    response_text += content

        elif name == "HuggingFace (Qwen)":
            # I use Qwen-2.5-72B here because it's a sheer powerhouse
            response_stream = await hf_client.chat_completion(
                model="Qwen/Qwen2.5-72B-Instruct",
                messages=[{"role": "user", "content": full_prompt}],
                max_tokens=600,
                stream=True,
            )
            async for chunk in response_stream:
                content = chunk.choices[0].delta.content
                if content:
                    if not silent:
                        print(f"{color_code}{content}\033[0m", end="", flush=True)
                    response_text += content

        elif name == "Ollama (Local)":
            # I talk to my local Ollama server over HTTPX
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST",
                    "http://localhost:11434/api/chat",
                    json={
                        "model": "llama3.1",
                        "messages": [{"role": "user", "content": full_prompt}],
                        "stream": True,
                        "options": {"num_predict": 600}
                    },
                    timeout=None
                ) as response:
                    async for line in response.aiter_lines():
                        if line:
                            body = json.loads(line)
                            content = body.get("message", {}).get("content", "")
                            if content:
                                if not silent:
                                    print(f"{color_code}{content}\033[0m", end="", flush=True)
                                response_text += content
                    
    except Exception as e:
        # If a provider fails (maybe I ran out of credits or they are down), I'll catch it here.
        # I mention the error but let the rest of my council keep moving!
        error_msg = f"[Note: I couldn't reach {name} right now. Error: {e}]"
        if not silent:
            print(f"{color_code}{error_msg}\033[0m")
        return None # I return None so I can skip this member in the debate flow
        
    if not silent:
        print() 
    return f"\n--- {name} ---\n{response_text}\n"

async def simulate_thinking(seconds=5):
    """I show a little spinner to let the user know my council is deep in thought."""
    print("\n\033[33m[ My council is deliberating intensely... ]\033[0m")
    chars = "/—\\"
    for i in range(seconds * 5):
        char = chars[i % len(chars)]
        sys.stdout.write(f"\r  {char} Thinking and sharing thoughts internally...")
        sys.stdout.flush()
        await asyncio.sleep(0.2)
    sys.stdout.write("\r  Done! Synthesis complete. Final verdict incoming...\n")

async def main():
    print("=====================================================")
    print("      Welcome to my Private AI Debate Council!       ")
    print("=====================================================")
    print("I've connected Gemini, Cohere, Groq, Ollama, OpenAI, HF, and NVIDIA.")
    print("My council will deliberate in private before sharing the results.")
    print("Type 'quit' to exit.")
    
    # I set up my council members with their color-coded IDs
    # I've added NVIDIA Nemotron to the front lines!
    council = [
        ("NVIDIA (Nemotron)", "\033[38;5;208m"), # Orange (256-color)
        ("Gemini (Google)", "\033[94m"),   # Blue
        ("Cohere (Command-R)", "\033[92m"), # Green
        ("Groq (Llama-3.1)", "\033[95m"),   # Magenta
        ("Ollama (Local)", "\033[96m"),     # Cyan
        ("OpenAI (GPT-4o)", "\033[93m"),    # Yellow
        ("HuggingFace (Qwen)", "\033[91m")  # Red
    ]
    
    while True:
        try:
            # I take the user's debate topic
            user_input = input("\n\033[1mTopic for Debate ('quit' to exit):\033[0m ").strip()
            if user_input.lower() == 'quit':
                print("Adjourning my council. See you next time!")
                break
            if not user_input:
                continue

            print(f"\n\033[1m\033[4m[ MY COUNCIL IS BEGINNING PRIVATE DELIBERATION ]\033[0m")
            
            # Phase 1: Opening Remarks (Silent)
            print("  Phase 1: Generating independent opening statements...")
            opening_remarks = []
            for name, color in council:
                try:
                    prompt = (
                        f"You are a member of my elite AI Council. The topic is: '{user_input}'\n"
                        "Provide your independent opening remarks. Keep it thorough but do not exceed 500 words. "
                        "Focus only on your own perspective for now."
                    )
                    remark = await stream_council_member(name, prompt, color, silent=True)
                    if remark:
                        opening_remarks.append(remark)
                except Exception as e:
                    print(f"\033[91m[Warning]: {name} dropped out of Phase 1. Error: {e}\033[0m")

            if not opening_remarks:
                print("\033[91m[Error]: None of my council members could respond. Please check my API keys!\033[0m")
                continue

            stage_1_transcript = "".join(opening_remarks)

            # Phase 2: Cross-Examination (Silent)
            print("  Phase 2: Formal cross-examination and critique...")
            critiques = []
            for name, color in council:
                try:
                    prompt = (
                        f"The debate topic is '{user_input}'.\nHere are the opening remarks from your peers:\n{stage_1_transcript}\n"
                        "I want you to critique their arguments, find the weak points, and defend your own perspective. "
                        "Limit this rebuttal to 500 words."
                    )
                    critique = await stream_council_member(name, prompt, color, silent=True)
                    if critique:
                        critiques.append(critique)
                except Exception as e:
                    print(f"\033[91m[Warning]: {name} failed to cross-examine. Error: {e}\033[0m")

            stage_2_transcript = "".join(critiques)

            # I add a 10-second pause for dramatic effect and "deliberation"
            await simulate_thinking(seconds=10)

            # Phase 3: The Verdict (PUBLIC)
            print(f"\n\n\033[1m\033[4m[ THE FINAL VERDICT: 5-BULLET SUMMARIES ]\033[0m")
            for name, color in council:
                try:
                    prompt = (
                        f"The debate on '{user_input}' is over.\n"
                        f"Peer critiques provided:\n{stage_2_transcript}\n\n"
                        "Give me your final, absolute conclusion. "
                        "YOU MUST OUTPUT EXACTLY 5 BULLET POINTS. "
                        "Keep the total under 500 words. Just the bullets—no intro or outro."
                    )
                    await stream_council_member(name, prompt, color, silent=False)
                except Exception as e:
                    print(f"\033[91m\n[Warning]: {name} couldn't deliver their verdict. Error: {e}\033[0m")

            print("\n=====================================================")
            print("                DELIBERATION COMPLETE                ")
            print("=====================================================")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\n[Critical System Failure]: {e}")
            print("I'm attempting to recover the council session...")

if __name__ == "__main__":
    # If I'm on Windows, I need to set the right loop policy for my async calls
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Fatal error during execution: {e}")
