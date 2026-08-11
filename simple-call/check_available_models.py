from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Models you can use for content generation:")
for model in client.models.list():
    if 'generateContent' in model.supported_actions:
        # The name you should use is the one that appears after 'models/'
        print(f"- {model.name.replace('models/', '')}")
