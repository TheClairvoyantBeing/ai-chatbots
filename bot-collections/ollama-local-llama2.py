#=========================================================================================
# My Local Ollama Terminal
#
# I use this to run powerful models like Llama 3.1 entirely on my own hardware. 
# No API keys needed, just total privacy.
#
# My Setup Checklist:
# 1. I download & install Ollama from https://ollama.com/
# 2. I pull my preferred model: ollama pull llama3.1
# 3. I keep the server running in the background and fire up this script!
#=========================================================================================

import requests
import json
import sys

def chat_with_ollama():
    # I point this to my local server's chat endpoint
    url = "http://localhost:11434/api/chat"
    
    # I can swap this for 'llama2', 'mistral', or whatever I've pulled via CLI
    model_name = "llama3.1"
    
    print(f"--- My Local Ollama Terminal ({model_name}) ---")
    print("I can type 'quit' to exit.\n")
    
    # I maintain my message history so the model remembers what we just said
    messages = []
    
    while True:
        # I wait for my input
        user_input = input("Me: ").strip()
        
        if user_input.lower() == 'quit':
            print("Shutting down my local AI. Goodbye!")
            break
            
        if not user_input:
            continue
            
        # I add my prompt to the conversation history
        messages.append({"role": "user", "content": user_input})
        
        # I set up my payload to stream responses back to me
        payload = {
            "model": model_name,
            "messages": messages,
            "stream": True
        }
        
        print("\nOllama: ", end="", flush=True)
        full_response = ""
        
        try:
            # I send a streaming POST request to my local server and watch the tokens roll in
            with requests.post(url, json=payload, stream=True) as response:
                response.raise_for_status()
                
                # I parse the response line by line as the tokens arrive from my hardware
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        if "message" in chunk:
                            content = chunk["message"].get("content", "")
                            print(content, end="", flush=True)
                            full_response += content
                        
                        if chunk.get("done"):
                            break
            
            # I save the AI's response in my history to keep the context alive
            messages.append({"role": "assistant", "content": full_response})
            print("\n")
            
        except requests.exceptions.ConnectionError:
            # If I forgot to start the server, I'll notify myself here
            print("\n[Oops]: I couldn't connect to my local Ollama server. Did I forget to start it?")
            print("[Tip]: I should try running 'ollama serve' in my terminal.")
            break
        except Exception as e:
            # I catch any other unexpected hiccups
            print(f"\n[My local system hit a snag]: {e}")
            break

if __name__ == "__main__":
    chat_with_ollama()
