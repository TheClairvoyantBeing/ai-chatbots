import os, asyncio
from google import genai
from dotenv import load_dotenv
from PIL import Image

# I load my environment and initialize Gemini
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def main():
    print("--- Gemini Terminal (2.5-Flash-Lite) ---")
    chat = client.aio.chats.create(model="gemini-2.5-flash-lite")

    while True:
        try:
            # I take my input and check if it's an image path
            user_input = input("\nMe: ").strip()
            if user_input.lower() == 'quit': break
            if not user_input: continue

            content = [user_input]
            parts = user_input.split(" ", 1)
            
            # I handle local images if provided
            if parts[0].lower().endswith(('.png', '.jpg', '.jpeg')) and os.path.exists(parts[0]):
                img = Image.open(parts[0])
                content = [img, parts[1] if len(parts) > 1 else "Describe this image."]

            print("\nGemini: ", end="", flush=True)
            async for chunk in await chat.send_message_stream(content):
                if chunk.text: print(chunk.text, end="", flush=True)
            print()

        except Exception as e:
            print(f"\n[Gemini Error]: {e}"); break

if __name__ == "__main__":
    asyncio.run(main())
