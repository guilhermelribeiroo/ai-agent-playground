from google import genai
import os
from dotenv import load_dotenv

# Initialize the client
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_ID = "gemini-flash-lite-latest" 
EMBEDDINGS_MODEL_ID = "models/gemini-embedding-2"

# Helper function: Calculates the proximity between two embeddings (Dot Product)
def calculate_similarity(vector1, vector2):
    return sum(a * b for a, b in zip(vector1, vector2))

# STEP 1: Your "Knowledge Base" (The documents)
documents = [
    "Our store's return policy allows returns within 30 days of purchase.",
    "Technical support operating hours are Monday through Friday, 9 AM to 6 PM.",
    "To reset your password, you must access the security settings panel in the app."
]

print("1. Generating embeddings for your documents...")
docs_embeddings = []
for doc in documents:
    # We use a specific Gemini model focused on turning text into numbers
    emb_response = client.models.embed_content(
        model=EMBEDDINGS_MODEL_ID, 
        contents=doc
    )
    docs_embeddings.append(emb_response.embeddings[0].values)

# STEP 2: The Question (Retrieval)
question = "How long do I have to return a product I bought?"
print(f"\n2. User asked: '{question}'")

# We transform the question into an embedding to search our "map"
question_response = client.models.embed_content(
    model=EMBEDDINGS_MODEL_ID,
    contents=question
)
question_embedding = question_response.embeddings[0].values

# Compare the question with all documents to find the most relevant one
best_score = -1
relevant_snippet = ""

for i, doc_emb in enumerate(docs_embeddings):
    score = calculate_similarity(question_embedding, doc_emb)
    if score > best_score:
        best_score = score
        relevant_snippet = documents[i]

print(f"   -> Snippet found in your database: '{relevant_snippet}'")

# STEP 3: Augmented Generation
# Now we combine the snippet we found with the original question and send it to Gemini!
final_prompt = f"""
You are a helpful assistant. Answer the user's question using ONLY the information provided in the document below.

Document: {relevant_snippet}
Question: {question}
"""

print("\n3. Sending context to Gemini to generate the final response...")
final_response = client.models.generate_content(
    model=MODEL_ID,
    contents=final_prompt
)

print(f"\nGemini: {final_response.text}")