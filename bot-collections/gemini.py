import os
import asyncio
from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image

# 1. I load my environment variables
load_dotenv()

# I initialize my new SDK Client. 
# I explicitly pass the key I loaded from my .env
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

async def main():
    print("Gemini Chatbot started! Type 'quit' to exit.")
    print("Tip: To send an image, type the full path to a .png or .jpg file, followed by your prompt.")
    print("Example: ./my_image.png What is in this picture?")
    
    # I start a chat session. Gemini natively handles history in the background!
    # I start an async chat session using the new syntax.
    # I use gemini-2.5-flash since it has a generous free tier limit and is extremely fast!
    chat = client.aio.chats.create(
        model="gemini-2.5-flash"
    )

    while True:
        try:
            user_input = input("\nPrompt ('quit' to exit): ").strip()
            
            # 1. I use clean Exit logic
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
                
            if not user_input:
                continue

            content_to_send = []
            
            # 2. Basic Vision Logic: I check if the first word looks like an image file
            parts = user_input.split(" ", 1)
            potential_file = parts[0]
            
            if potential_file.lower().endswith(('.png', '.jpg', '.jpeg')) and os.path.exists(potential_file):
                print(f"[Loading image: {potential_file}...]")
                try:
                    # I open my image using Pillow (PIL)
                    img = Image.open(potential_file)
                    content_to_send.append(img)
                    
                    # If my user typed text after the image path, I add it as the prompt
                    if len(parts) > 1:
                        content_to_send.append(parts[1])
                    else:
                        content_to_send.append("Please describe this image.")
                except Exception as e:
                    print(f"Failed to load image: {e}")
                    content_to_send.append(user_input)
            else:
                # I just use a normal text prompt
                content_to_send.append(user_input)

            # 3. I call my Gemini API (New SDK handles async/streams differently)
            response_stream = await chat.send_message_stream(content_to_send)
            
            print("\nGemini: ", end="", flush=True)
            bot_reply = ""
            async for chunk in response_stream:
                if chunk.text:
                    print(chunk.text, end="", flush=True)
                    bot_reply += chunk.text
            print() # Print a newline after the stream finishes

        except KeyboardInterrupt:
            # I handle Ctrl+C gracefully
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAPI Error: {e}")

if __name__ == "__main__":
    # 4. I use clean async execution
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Fatal error: {e}")
