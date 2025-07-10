import faiss
import openai
import numpy as np
import json
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

MODEL_EMBEDDING = "text-embedding-3-small"  # or "text-embedding-ada-002"
EMBED_DIM = 1536  # 3072 for text-embedding-3-large
MODEL_CHAT = "gpt-4o"  # or "gpt-3.5-turbo"

INDEX_FILE = "faiss_index.index"
METADATA_FILE = "metadata.json"

SYSTEM_PROMPT = """
You are an expert on the Ninjamock platform and are helping the user understand how to use its features.
Respond clearly and concisely, using only the information provided in context.
If you don't know something, say you're not sure.
"""

# === FUNCTIONS ===
def load_index_and_metadata():
    index = faiss.read_index(INDEX_FILE)
    with open(METADATA_FILE, "r", encoding="utf-8") as file:
        metadata = json.load(file)
    return index, metadata

def embed_query(query, model=MODEL_EMBEDDING):
    response = openai.embeddings.create(
        input=[query],
        model=model
    )
    return np.array(response.data[0].embedding).astype("float32")

def retrieve_relevant_chunks(query,top_k=5):
    index, metadata = load_index_and_metadata()
    query_vector = embed_query(query).reshape(1, -1)
    distances, indices = index.search(query_vector, min(top_k,len(metadata)))

    chunks = []
    for i, idx in enumerate(indices[0]):
        if idx < len(metadata):
            chunk = metadata[idx]
            chunks.append({
                "score": float(distances[0][i]),
                "title": chunk["title"],
                "text": chunk["text"],
            })
    return chunks

def build_context(chunks):
    context = ""
    for i, chunk in enumerate(chunks,1):
        context += f"[{i}] {chunk['title']}:\n{chunk['text']}\n\n"
    return context.strip()

def ask_openai(question, context):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]
    response = openai.chat.completions.create(
        model=MODEL_CHAT,
        messages=messages,
        temperature=0.3
    )

    return response.choices[0].message.content.strip()
def get_context_from_query(query):
    """
    Retrieves relevant chunks based on the query and builds a context string.
    """
    print("Retrieving relevant chunks...")
    chunks = retrieve_relevant_chunks(query)
    
    if not chunks:
        return "No relevant information found."

    print(f"Found {len(chunks)} relevant chunks.")
    context = build_context(chunks)
    return context
# === MAIN ===
if __name__ == "__main__":
    while True:
        query = input("Enter your question (or 'exit' to quit): ").strip()
        if query.lower() == "exit":
            break

        print("Retrieving relevant information...")
        chunks = retrieve_relevant_chunks(query)

        for i, c in enumerate(chunks, 1):
            print(f"[{i}] Title: {c['title']}")
            print(f"    Score: {c['score']:.4f}")
            print(f"    Text: {c['text'][:300]}...\n")
        
        context = build_context(chunks)

        print("Asking OpenAI...")
        answer = ask_openai(query, context)
        print(f"Answer: {answer}\n")