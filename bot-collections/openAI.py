#=======================================
# Use : pip install openai python-dotenv
#======================================

import os
from openai import OpenAI
from dotenv import load_dotenv

# I will automatically find my .env file in the parent directory and load it
load_dotenv()

# My client will automatically use the OPENAI_API_KEY from my environment
client = OpenAI()

user_prompt = input("Prompt: ")
system_prompt = "Limit your answer to one sentence. Pretend you're a cat."

# I use the corrected API call format for OpenAI Chat Completions
response = client.chat.completions.create(
    model="gpt-4o", # Or gpt-3.5-turbo
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
)

# I print my actual text response
print(response.choices[0].message.content)