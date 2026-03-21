# AI Chatbot Collection & Council

A high-performance repository of CLI-based chatbots and a multi-model debate council. This project hits raw API streams for speed, privacy, and full control over leading LLMs.

---

## 🚀 Getting Started

### 1. Simple Setup
```bash
# I recommend using a virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Mac/Linux

# Install all dependencies
pip install -r requirements.txt
```

### 2. Configure Your Keys
Create a `.env` file in the root with your API keys:
```env
GEMINI_API_KEY="your_key"
HF_API_KEY="your_key"
COHERE_API_KEY="your_key"
GROQ_API_KEY="your_key"
OPENAI_API_KEY="your_key"
NVIDIA_API_KEY="your_key"
```

### 3. Verify Everything
Diagnostic tools to ensure setup is perfect:
*   **`python test_all_apis.py`**: Pings every provider (Gemini, Groq, OpenAI, etc.) and reports success status.
*   **`python test_hf.py`**: Locates active free-tier models on HuggingFace.

---

## 🤖 How to Use

### Individual Chatbots
Every bot in `bot-collections/` features real-time streaming:
```bash
python bot-collections/gemini.py
python bot-collections/openAI.py
python bot-collections/groq_bot.py
# ... and more
```

### The AI Council (Debate Mode)
Multi-model deliberation for complex topics:
```bash
python ai-panel/ai-council.py
```

---

## 🏁 What to Expect at the End

The following captures demonstrate the final refined output across different models:

💠 **Smart Chat** (Cohere)
![Cohere Showcase](./screenshots/cohere-1.png)

💠 **Vision Bot** (Gemini)
![Gemini Showcase](./screenshots/Gemini--2.png)

💠 **Fast Brain** (Groq)
![Groq Showcase](./screenshots/Groq-1.png)

💠 **Thinking Mode** (NVIDIA)
![NVIDIA Showcase](./screenshots/nvidia-nemotron-1.png)

💠 **Local Brain** (Ollama)
![Ollama Showcase](./screenshots/ollama-local-llama.png)

---
*Developed as a modular framework for private and high-speed AI interaction.*
