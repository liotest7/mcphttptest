import faiss
import openai
import json
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
INDEX_FILE = "faiss_index.index"
METADATA_FILE = "metadata.json"
MODEL = "text-embedding-3-small" # o "text-embedding-ada-002"
EMBED_DIM = 1536  # 3072 for text-embedding-3-large

# === FUNCTIONS ===

def load_index_and_metadata():
    index = faiss.read_index(INDEX_FILE)
    with open(METADATA_FILE, "r", encoding="utf-8") as file:
        metadata = json.load(file)
    return index, metadata

def embed_query(query, model=MODEL):
    response = openai.embeddings.create(
        input=[query],
        model=model
    )
    return np.array(response.data[0].embedding).astype("float32")

def search(query,top_k=5):
    index,metadata = load_index_and_metadata()
    query_vector = embed_query(query).reshape(1, -1)
    distances, indices = index.search(query_vector, top_k)

    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(metadata):
            results.append({
                "score": float(distances[0][i]),
                "title": metadata[idx]["title"],
                "text": metadata[idx]["text"],
            })
    return results

# === MAIN ===
if __name__ == "__main__":
    while True:
        query = input("Enter your search query (or 'exit' to quit): ")
        if query.lower() == "exit":
            break
        results = search(query)
        print(f"Found {len(results)} results for query: '{query}'")
        for i, r in enumerate(results, 1):
            print(f"[{i}] Título: {r['title']}")
            print(f"    Puntaje: {r['score']:.4f}")
            print(f"    Texto: {r['text']}...\n")