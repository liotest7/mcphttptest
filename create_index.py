import json
import faiss
import numpy as np
import openai
import tiktoken
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "text-embedding-3-small"
EMBED_DIM = 1536 # 3072 for text-embedding-3-large

def load_articles(json_file="articles.json"):
    with open(json_file, "r", encoding="utf-8") as file:
        return json.load(file)
    
def count_tokens(text,model="gpt-4o"):
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    return len(tokens)

def chunk_text(text, max_tokens=300):
    sentences = text.splitlines()
    chunks = []
    current = ""
    
    for sentence in sentences:
        # Asegurarse de que hay un espacio entre frases
        if count_tokens(current + sentence) > max_tokens:
            if current.strip():
                chunks.append(current.strip())
                current = ""
        current += sentence + "\n"

    if current.strip():
        chunks.append(current.strip())

    return chunks


def embed_text(texts, model=MODEL):
    embeddings = []
    batch_size = 100
    for i in range(0, len(texts), batch_size):
        response = openai.embeddings.create(
            input=texts[i:i + batch_size],
            model=model
        )
        batch_embeddings = [e.embedding for e in response.data]
        embeddings.extend(batch_embeddings)
    return embeddings

# === MAIN ===

def build_faiss_index(articles):
    all_texts = []
    metadata = []

    for article in articles:
        title = article["title"]
        chunks = chunk_text(article["text"])
        for i, chunk in enumerate(chunks):
            all_texts.append(chunk)
            metadata.append({
                "title": title,
                  "chunk_index": i,
                  "text": chunk
                  })
            
    print(f"Total chunks: {len(all_texts)}")

    print("Embedding texts...")
    embeddings = embed_text(all_texts)

    print("Creating FAISS index...")
    index = faiss.IndexFlatL2(EMBED_DIM)
    index.add(np.array(embeddings).astype('float32'))

    #save index and metadata
    faiss.write_index(index, "faiss_index.index")
    with open("metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)

    print("index FAISS index created and saved as 'faiss_index.index'")

# === EXECUTION ===
if __name__ == "__main__":
    articles = load_articles()
    build_faiss_index(articles)
    print("Indexing completed.")