#=============================================
# My Google Gemini Chatbot
# Use : pip install google-genai Pillow python-dotenv
#=============================================

import os
import asyncio
from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image

# I load my environment variables
load_dotenv()

# I initialize my Gemini SDK Client. 
# I explicitly pass the key I loaded from my .env
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

async def main():
    print("--- My Google Gemini Chatbot (gemini-2.5-flash) ---")
    print("Type 'quit' to exit.")
    print("Tip: I can analyze images! Type the full path to a .png or .jpg file, followed by your prompt.")
    
    # I start a chat session. Gemini natively handles history in the background!
    # I use gemini-2.5-flash for speed and generous free-tier limits.
    chat = client.aio.chats.create(
        model="gemini-2.5-flash"
    )

    while True:
        try:
            # I take my user input
            user_input = input("\nMe: ").strip()
            
            if user_input.lower() == 'quit':
                print("Shutting down my Gemini bot. Goodbye!")
                break
                
            if not user_input:
                continue

            content_to_send = []
            
            # I check if the first word is a path to an image file
            parts = user_input.split(" ", 1)
            potential_file = parts[0]
            
            if potential_file.lower().endswith(('.png', '.jpg', '.jpeg')) and os.path.exists(potential_file):
                print(f"[I am loading my image: {potential_file}...]")
                try:
                    # I open my image using Pillow (PIL)
                    img = Image.open(potential_file)
                    content_to_send.append(img)
                    
                    # If I typed text after the image path, I use it as my prompt
                    if len(parts) > 1:
                        content_to_send.append(parts[1])
                    else:
                        content_to_send.append("Please describe this image.")
                except Exception as e:
                    print(f"Failed to load my image: {e}")
                    content_to_send.append(user_input)
            else:
                # I just send a normal text prompt
                content_to_send.append(user_input)

            # I call my Gemini API with real-time streaming enabled
            response_stream = await chat.send_message_stream(content_to_send)
            
            print("\nGemini: ", end="", flush=True)
            bot_reply = ""
            
            # I iterate through my incoming chunks
            async for chunk in response_stream:
                if chunk.text:
                    print(chunk.text, end="", flush=True)
                    bot_reply += chunk.text
            print() 

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\n[API Error]: {e}")

if __name__ == "__main__":
    # I use clean async execution
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Fatal error: {e}")
