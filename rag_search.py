import faiss
import openai
import json
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "text-embedding-3-small"
EMBED_DIM = 1536

def load_index_and_metadata(index_path, metadata_path):
    index = faiss.read_index(index_path)
    with open(metadata_path, "r", encoding="utf-8") as file:
        metadata = json.load(file)
    return index, metadata

def embed_query(query, model=MODEL):
    response = openai.embeddings.create(
        input=[query],
        model=model
    )
    return np.array(response.data[0].embedding).astype("float32")

def search_rag(query, index_path, metadata_path, top_k=5):
    index, metadata = load_index_and_metadata(index_path, metadata_path)
    query_vector = embed_query(query).reshape(1, -1)
    distances, indices = index.search(query_vector, top_k)
    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(metadata):
            doc = metadata[idx]
            results.append({
                "score": float(distances[0][i]),
                "title": doc.get("title"),
                "text": doc.get("text"),
                "id": doc.get("id"),
                "type": doc.get("type"),
                "category": doc.get("category"),
                "templateId": doc.get("templateId"),
                "author": doc.get("author"),
                "tags": doc.get("tags"),
                "properties": doc.get("properties"),
                "children": doc.get("children"),
                "defaultProperties": doc.get("defaultProperties")
            })
    return results

# === MAIN ===
if __name__ == "__main__":
    index_path = input("Path to FAISS index: ").strip()
    metadata_path = input("Path to metadata JSON: ").strip()
    while True:
        query = input("Enter your search query (or 'exit' to quit): ")
        if query.lower() == "exit":
            break
        results = search_rag(query, index_path, metadata_path)
        print(f"Found {len(results)} results for query: '{query}'")
        for i, r in enumerate(results, 1):
            print(f"[{i}] Título: {r['title']}")
            print(f"    Puntaje: {r['score']:.4f}")
            print(f"    Texto: {r['text']}...\n")
