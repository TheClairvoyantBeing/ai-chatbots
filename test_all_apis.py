import asyncio, os, httpx, json
from dotenv import load_dotenv
from google import genai
import cohere
from groq import AsyncGroq
from openai import AsyncOpenAI
from huggingface_hub import AsyncInferenceClient

load_dotenv()

results = []

def log_result(provider, model, status, details=""):
    results.append({
        "Provider": provider,
        "Model": model,
        "Status": "✅ SUCCESS" if status else "❌ FAILED",
        "Details": details
    })

async def test_gemini():
    p, m = "Gemini", "gemini-2.5-flash-lite"
    print(f"Testing {p}...", end=" ", flush=True)
    try:
        key = os.getenv("GEMINI_API_KEY")
        if not key: raise Exception("Key Missing")
        client = genai.Client(api_key=key)
        if client.models.generate_content(model=m, contents="hi").text:
            print("✅"); log_result(p, m, True, "Response received"); return
    except Exception as e: print("❌"); log_result(p, m, False, str(e))

async def test_cohere():
    p, m = "Cohere", "command-a-03-2025"
    print(f"Testing {p}...", end=" ", flush=True)
    try:
        key = os.getenv("COHERE_API_KEY")
        if not key: raise Exception("Key Missing")
        client = cohere.AsyncClientV2(api_key=key)
        if (await client.chat(model=m, messages=[{"role": "user", "content": "hi"}])).message.content:
            print("✅"); log_result(p, m, True, "Response received"); return
    except Exception as e: print("❌"); log_result(p, m, False, str(e))

async def test_groq():
    p, m = "Groq", "llama-3.1-8b-instant"
    print(f"Testing {p}...", end=" ", flush=True)
    try:
        key = os.getenv("GROQ_API_KEY")
        if not key: raise Exception("Key Missing")
        client = AsyncGroq(api_key=key)
        if (await client.chat.completions.create(model=m, messages=[{"role": "user", "content": "hi"}], max_tokens=10)).choices[0].message.content:
            print("✅"); log_result(p, m, True, "Response received"); return
    except Exception as e: print("❌"); log_result(p, m, False, str(e))

async def test_openai():
    p, m = "OpenAI", "gpt-4o"
    print(f"Testing {p}...", end=" ", flush=True)
    try:
        key = os.getenv("OPENAI_API_KEY")
        if not key: raise Exception("Key Missing")
        client = AsyncOpenAI(api_key=key)
        if (await client.chat.completions.create(model=m, messages=[{"role": "user", "content": "hi"}], max_tokens=10)).choices[0].message.content:
            print("✅"); log_result(p, m, True, "Response received"); return
    except Exception as e: print("❌"); log_result(p, m, False, str(e))

async def test_nvidia():
    p, m = "NVIDIA", "nvidia/nemotron-3-nano-30b-a3b"
    print(f"Testing {p}...", end=" ", flush=True)
    try:
        key = os.getenv("NVIDIA_API_KEY")
        if not key: raise Exception("Key Missing/Invalid")
        client = AsyncOpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=key)
        if (await client.chat.completions.create(model=m, messages=[{"role": "user", "content": "hi"}], max_tokens=10)).choices[0].message.content:
            print("✅"); log_result(p, m, True, "Response received"); return
    except Exception as e: print("❌"); log_result(p, m, False, str(e))

async def test_huggingface():
    p, m = "HuggingFace", "Qwen/Qwen2.5-72B-Instruct"
    print(f"Testing {p}...", end=" ", flush=True)
    try:
        key = os.getenv('HF_API_KEY')
        if not key: raise Exception("Key Missing")
        client = AsyncInferenceClient(token=key)
        res = await client.chat_completion(model=m, messages=[{'role': 'user', 'content': 'hi'}], max_tokens=10)
        if res.choices and len(res.choices) > 0:
            print("✅"); log_result(p, m, True, "Response received"); return
    except Exception as e: print("❌"); log_result(p, m, False, str(e))

async def test_ollama():
    p, m = "Ollama", "llama3.1"
    print(f"Testing {p}...", end=" ", flush=True)
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post("http://localhost:11434/api/chat", json={"model": m, "messages": [{"role": "user", "content": "hi"}], "stream": False}, timeout=5.0)
            if res.status_code == 200:
                print("✅"); log_result(p, m, True, "Local server active"); return
        raise Exception(f"Status Code {res.status_code}")
    except Exception as e: print("❌"); log_result(p, m, False, str(e))

async def main():
    print("--- Starting AI API Sequential Diagnostic (March 2026) ---\n")
    
    await test_gemini()
    await test_cohere()
    await test_groq()
    await test_openai()
    await test_nvidia()
    await test_huggingface()
    await test_ollama()

    print("\n" + "="*80)
    print(f"{'PROVIDER':<15} | {'MODEL':<30} | {'STATUS':<12} | {'DETAILS'}")
    print("-" * 80)
    for res in results:
        details = (res["Details"][:30] + "..") if len(res["Details"]) > 32 else res["Details"]
        print(f"{res['Provider']:<15} | {res['Model']:<30} | {res['Status']:<12} | {details}")
    print("="*80 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
