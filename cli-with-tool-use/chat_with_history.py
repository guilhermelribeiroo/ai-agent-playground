from google import genai
from google.genai import types
import os
import time
from dotenv import load_dotenv

# Load API Key
load_dotenv()
# Initialize Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_ID = "gemini-flash-lite-latest"

# Maintain our manual interaction history
interactions_history = []

def send_message(user_text: str) -> str:
    # Package the user's input
    user_content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=user_text)]
    )
    
    # Send the full array to the API
    print(f"Sending request to {MODEL_ID}...")
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=interactions_history + [user_content]
    )
    
    # If successful, save both the user prompt and model response to history
    model_content = types.Content(
        role="model",
        parts=[types.Part.from_text(text=response.text)]
    )
    
    interactions_history.extend([user_content, model_content])
    return response.text

# --- Test the Flow ---
if __name__ == "__main__":
    try:
        print("Turn 1:", send_message("Hi, my favorite fruit is the pineapple."))
        print("-" * 40)
        print("Turn 2:", send_message("What is my favorite fruit?"))
    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")