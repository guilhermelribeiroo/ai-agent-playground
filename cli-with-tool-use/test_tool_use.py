from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 1. Define your "tool"
# The model uses Type Hinting (str) and the Docstring (""") to understand what the function does.
def query_cep(cep: str) -> str:
    """Queries a Brazilian CEP (zip code) and returns the corresponding address."""
    print(f"\n[SYSTEM: Executing the 'query_cep' tool for CEP: {cep}]")
    
    # In a real-world scenario, you would make an HTTP request to an external API here.
    if cep == "01001-000":
        return "Praça da Sé, São Paulo - SP"
    return "CEP not found."

# 2. Initialize the client
client = genai.Client()

MODEL_ID = "gemini-flash-lite-latest" 

# 3. Configure the call to include the tool
print("User: Can you tell me what the address is for the CEP 01001-000?")
response = client.models.generate_content(
    model=MODEL_ID,
    contents="Can you tell me what the address is for the CEP 01001-000?",
    config=types.GenerateContentConfig(
        tools=[query_cep], 
    )
)

print(f"\nGemini: {response.text}")