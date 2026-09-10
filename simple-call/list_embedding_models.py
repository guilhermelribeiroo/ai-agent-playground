from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Available embedding models for your account:\n")
for model in client.models.list():
    # Filtering only for models that have 'embed' in their name
    if "embed" in model.name.lower():
        print(f"- {model.name}")