#=========================================================================================
# My Local Ollama Chatbot - Llama 2 / Llama 3.1
#
# To use this bot, I must have the Ollama server running on my machine. 
#
# My Setup Commands:
# 1. Download & Install: https://ollama.com/
# 2. Start the server (usually runs in background tray)
# 3. Pull my model (Open terminal and run): ollama pull llama3.1
# 4. Start the bot: python bot-collections/ollama-local-llama2.py
#=========================================================================================

import requests
import json
import sys

def chat_with_ollama():
    # I set the local endpoint for my Ollama API
    url = "http://localhost:11434/api/chat"
    
    # I can change this to 'llama2' or any other model I have pulled via command line
    model_name = "llama3.1"
    
    print(f"--- My Local Ollama Chatbot ({model_name}) ---")
    print("Type 'quit' to exit.\n")
    
    # I maintain my message history for a continuous conversation
    messages = []
    
    while True:
        # I take my user input
        user_input = input("Me: ").strip()
        
        if user_input.lower() == 'quit':
            print("Shutting down my local AI. Goodbye!")
            break
            
        if not user_input:
            continue
            
        # I append my message to the conversation history
        messages.append({"role": "user", "content": user_input})
        
        # I prepare my payload for the Ollama stream
        payload = {
            "model": model_name,
            "messages": messages,
            "stream": True
        }
        
        print("\nOllama: ", end="", flush=True)
        full_response = ""
        
        try:
            # I send a streaming POST request to my local server
            with requests.post(url, json=payload, stream=True) as response:
                response.raise_for_status()
                
                # I process the response line by line as it streams tokens
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        if "message" in chunk:
                            content = chunk["message"].get("content", "")
                            print(content, end="", flush=True)
                            full_response += content
                        
                        if chunk.get("done"):
                            break
            
            # I save the AI's response to my history so it remembers the context
            messages.append({"role": "assistant", "content": full_response})
            print("\n")
            
        except requests.exceptions.ConnectionError:
            print("\n[Error]: I couldn't connect to Ollama. Is my Ollama server running?")
            print("[Cmd]: Try running 'ollama serve' in a terminal.")
            break
        except Exception as e:
            print(f"\n[An unexpected error occurred]: {e}")
            break

if __name__ == "__main__":
    chat_with_ollama()
