from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print(f"{'MODEL NAME':<30} | {'Supported Actions'}")
print("-" * 80)

# List the models
for model in client.models.list():
    # The supported actions indicate whether the model is suitable for chat (generateContent), 
    # search (embedContent), etc.
    actions = ", ".join(model.supported_actions)
    print(f"{model.name:<30} | {actions}")