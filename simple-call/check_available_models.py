from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Modelos que você pode usar para gerar conteúdo:")
for model in client.models.list():
    if 'generateContent' in model.supported_actions:
        # O nome que você deve usar é o que aparece após 'models/'
        print(f"- {model.name.replace('models/', '')}")
