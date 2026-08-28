from google import genai
import os
import time
from dotenv import load_dotenv

# Load API Key
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_ID = "gemini-flash-lite-latest"

def start_new_chat():
    print(f"\n--- Starting a new session ({MODEL_ID}) ---")
    # Adding a system instruction to force English responses
    return client.chats.create(
        model=MODEL_ID,
        config={'system_instruction': 'Please respond always in English.'}
    )

chat = start_new_chat()

print("--- Gemini CLI Chat ---")
print("Type your message or 'exit' to quit.")

while True:
    user_input = input("\nYou: ")
    
    if user_input.lower() in ['exit', 'quit']:
        print("Goodbye!")
        break
        
    if not user_input.strip():
        continue

    try:
        # Sending message to Gemini
        response = chat.send_message(user_input)
        print(f"Gemini: {response.text}")

    except Exception as e:
        error_msg = str(e)
        
        if "429" in error_msg:
            print("\n[ERROR] Quota exceeded. Please wait 30 seconds...")
            time.sleep(30)
        elif "400" in error_msg:
            print("\n[ERROR] Invalid sequence or corrupted history. Resetting chat...")
            chat = start_new_chat()
        else:
            print(f"\n[UNEXPECTED ERROR] {error_msg}")
            print("Resetting session...")
            chat = start_new_chat()