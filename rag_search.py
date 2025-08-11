import faiss
import openai
import json
import numpy as np
from dotenv import load_dotenv
import os
from typing import List, Dict, Optional, Tuple

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "text-embedding-3-small"
EMBED_DIM = 1536

def load_index_and_metadata(index_path, metadata_path):
    index = faiss.read_index(index_path)
    with open(metadata_path, "r", encoding="utf-8") as file:
        metadata = json.load(file)
    return index, metadata

def _offsets_path(jsonl_path: str) -> str:
    return jsonl_path + ".offsets"

def build_jsonl_offsets(jsonl_path: str, offsets_path: Optional[str] = None) -> List[int]:
    """
    Build and cache byte offsets for each line in a JSONL file to enable O(1) random access.
    Returns the list of line-start offsets. Safe to use on large files.
    """
    path = offsets_path or _offsets_path(jsonl_path)
    # If offsets cache exists, load it
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            # Fall through to rebuild
            pass

    offsets: List[int] = []
    pos = 0
    with open(jsonl_path, "rb") as f:
        while True:
            offsets.append(pos)
            line = f.readline()
            if not line:
                # Last append will be EOF; remove if file ended exactly at previous line end
                offsets.pop()
                break
            pos += len(line)

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(offsets, f)
    except Exception:
        # Cache write failure is non-fatal
        pass
    return offsets

def get_jsonl_row(jsonl_path: str, offsets: List[int], idx: int) -> Optional[Dict]:
    if idx < 0 or idx >= len(offsets):
        return None
    with open(jsonl_path, "rb") as f:
        f.seek(offsets[idx])
        line = f.readline()
    try:
        return json.loads(line.decode("utf-8"))
    except Exception:
        return None

def load_index_and_jsonl(index_path: str, jsonl_path: str) -> Tuple[faiss.Index, List[int]]:
    index = faiss.read_index(index_path)
    offsets = build_jsonl_offsets(jsonl_path)
    return index, offsets

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
            # Start with the score, then merge all fields from doc to preserve arbitrary metadata
            result = {"score": float(distances[0][i])}
            if isinstance(doc, dict):
                result.update(doc)
            else:
                result["text"] = str(doc)
            results.append(result)
    return results

def search_rag_jsonl(query: str, index_path: str, jsonl_path: str, top_k: int = 5) -> List[Dict]:
    """
    Modern and robust RAG search using FAISS + JSONL metadata.
    - Uses a byte-offset cache for O(1) random access on JSONL rows.
    - Merges arbitrary fields from each JSONL object into the result alongside the distance score.
    - Validates index size vs JSONL length and gracefully handles mismatches.
    """
    index, offsets = load_index_and_jsonl(index_path, jsonl_path)
    query_vector = embed_query(query).reshape(1, -1)
    top_k = max(1, int(top_k))
    distances, indices = index.search(query_vector, top_k)

    # If FAISS index has fewer vectors than requested, clamp
    nvec = getattr(index, 'ntotal', len(offsets))
    max_valid = min(nvec, len(offsets))

    results: List[Dict] = []
    for i, idx in enumerate(indices[0]):
        if idx is None:
            continue
        if idx < 0 or idx >= max_valid:
            continue
        doc = get_jsonl_row(jsonl_path, offsets, int(idx))
        result = {"score": float(distances[0][i])}
        if isinstance(doc, dict):
            result.update(doc)
        elif doc is not None:
            result["text"] = str(doc)
        results.append(result)
    return results

# === MAIN ===
if __name__ == "__main__":
    index_path = input("Path to FAISS index: ").strip()
    meta_path = input("Path to metadata (JSON array or JSONL): ").strip()
    while True:
        query = input("Enter your search query (or 'exit' to quit): ")
        if query.lower() == "exit":
            break
        if meta_path.lower().endswith(".jsonl"):
            results = search_rag_jsonl(query, index_path, meta_path)
        else:
            results = search_rag(query, index_path, meta_path)
        print(f"Found {len(results)} results for query: '{query}'")
        for i, r in enumerate(results, 1):
            title = r.get('title') or r.get('section') or '(no title)'
            text = r.get('text', '')
            print(f"[{i}] Title: {title}")
            print(f"    Score: {r['score']:.4f}")
            if text:
                print(f"    Text: {text[:240]}...\n")
