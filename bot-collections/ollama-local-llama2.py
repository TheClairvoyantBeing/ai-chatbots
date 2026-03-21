import requests, json

# I connect to my local Ollama server
def chat_with_ollama():
    url = "http://localhost:11434/api/chat"
    model_name = "llama3.1"
    
    print(f"--- Local Ollama Terminal ({model_name}) ---")
    print("I can type 'quit' to exit.\n")
    
    messages = []
    
    while True:
        try:
            # I wait for my input
            user_input = input("Me: ").strip()
            if user_input.lower() == 'quit': break
            if not user_input: continue
            
            messages.append({"role": "user", "content": user_input})
            print("\nOllama: ", end="", flush=True)
            full_response = ""
            
            # I send a streaming POST request to my local hardware
            with requests.post(url, json={"model": model_name, "messages": messages, "stream": True}, stream=True) as response:
                response.raise_for_status()
                
                # I parse and print tokens as they arrive
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        content = chunk.get("message", {}).get("content", "")
                        print(content, end="", flush=True)
                        full_response += content
                        if chunk.get("done"): break
            
            messages.append({"role": "assistant", "content": full_response})
            print("\n")
            
        except Exception as e:
            print(f"\n[Ollama Error]: {e}"); break

if __name__ == "__main__":
    chat_with_ollama()
