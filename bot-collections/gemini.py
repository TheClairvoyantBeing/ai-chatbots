#=========================================================================================
# My Google Gemini Vision-Terminal
# 
# I use this to interact with Gemini-1.5-Flash. It's incredibly fast and 
# natively handles images if I provide a local file path.
#=========================================================================================

import os
import asyncio
from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image

# I load my environment variables
load_dotenv()

# I initialize my Gemini SDK Client using my secret API key
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

async def main():
    print("--- My Google Gemini Terminal (gemini-2.5-flash) ---")
    print("I can type 'quit' to exit.")
    print("Pro Tip: I can analyze images! I just type the file path (.png/.jpg) followed by my question.")
    
    # I start a chat session. Gemini natively handles history for me!
    # I'm using gemini-2.5-flash because it's efficient and has generous free limits.
    chat = client.aio.chats.create(
        model="gemini-2.5-flash"
    )

    while True:
        try:
            # I wait for my input
            user_input = input("\nMe: ").strip()
            
            if user_input.lower() == 'quit':
                print("Closing my Gemini terminal. Goodbye!")
                break
                
            if not user_input:
                continue

            content_to_send = []
            
            # I check if I'm trying to send an image file path first
            parts = user_input.split(" ", 1)
            potential_file = parts[0]
            
            if potential_file.lower().endswith(('.png', '.jpg', '.jpeg')) and os.path.exists(potential_file):
                print(f"[I'm loading my image from: {potential_file}...]")
                try:
                    # I open the image using Pillow so Gemini can "see" it
                    img = Image.open(potential_file)
                    content_to_send.append(img)
                    
                    # If I added text after my image path, I'll use it as the prompt
                    if len(parts) > 1:
                        content_to_send.append(parts[1])
                    else:
                        content_to_send.append("Please describe this image for me.")
                except Exception as e:
                    print(f"I failed to load the image: {e}")
                    content_to_send.append(user_input)
            else:
                # Otherwise, I just send a normal text query
                content_to_send.append(user_input)

            # I call the Gemini API with real-time streaming enabled
            response_stream = await chat.send_message_stream(content_to_send)
            
            print("\nGemini: ", end="", flush=True)
            bot_reply = ""
            
            # I iterate through the stream and print the text as it arrives
            async for chunk in response_stream:
                if chunk.text:
                    print(chunk.text, end="", flush=True)
                    bot_reply += chunk.text
            print() 

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            # I catch API errors or connectivity issues here
            print(f"\n[Gemini System Alert]: {e}")

if __name__ == "__main__":
    # I start the async main loop
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"My Gemini terminal encountered a fatal error: {e}")
