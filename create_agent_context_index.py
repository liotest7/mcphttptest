import os
import re
import json
from typing import List, Dict, Tuple

import faiss
import numpy as np
import openai
import tiktoken
from dotenv import load_dotenv

# Config
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "text-embedding-3-small"
EMBED_DIM = 1536

SOURCE_PATH = "data/agent_context.md"
OUT_DIR = "indices/agent_context"
INDEX_PATH = os.path.join(OUT_DIR, "faiss_index.index")
METADATA_JSON_PATH = os.path.join(OUT_DIR, "metadata.json")
CHUNKS_JSONL_PATH = os.path.join(OUT_DIR, "chunks.jsonl")

# Chunking params
CHUNK_SIZE_TOKENS = 700  # target size ~500–800 tokens
OVERLAP_CHARS = 180      # ~150–200 characters overlap


# Utilities
encoding = tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str) -> int:
    return len(encoding.encode(text))

def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text


def read_markdown(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def split_sections(md: str) -> List[Dict]:
    """Split markdown into sections by ## and ### headings.
    Returns list of {heading, level, content} items.
    """
    lines = md.splitlines()
    sections: List[Dict] = []
    current = {"heading": None, "level": None, "content": []}

    def push_current():
        if current["heading"] is not None:
            sections.append({
                "heading": current["heading"],
                "level": current["level"],
                "content": "\n".join(current["content"]).strip()
            })

    for line in lines:
        if line.startswith("### ") or line.startswith("## "):
            # new section
            level = 3 if line.startswith("### ") else 2
            heading = line[4:] if level == 3 else line[3:]
            # push previous
            push_current()
            # init new
            current = {"heading": heading.strip(), "level": level, "content": []}
        else:
            # skip top-level # title from being part of previous None section
            if current["heading"] is None:
                # find first ## or ###; until then ignore
                continue
            current["content"].append(line)

    # push last
    push_current()
    return sections


def paragraph_split(text: str) -> List[str]:
    # split by blank lines but keep code fences together
    parts = re.split(r"\n\s*\n", text.strip())
    # normalize whitespace
    return [p.strip() for p in parts if p.strip()]


def split_long_paragraph(p: str, target_tokens: int, overlap_chars: int) -> List[str]:
    # fallback: character windowing when a single paragraph is too long
    # rough char budget: assume ~4 chars/token average for English; use 4 as heuristic
    approx_chars = max(400, target_tokens * 4)
    out: List[str] = []
    start = 0
    while start < len(p):
        end = min(len(p), start + approx_chars)
        out.append(p[start:end])
        if end >= len(p):
            break
        start = max(start + approx_chars - overlap_chars, 0)
    return out


def chunk_section(heading: str, level: int, content: str) -> List[str]:
    paras = paragraph_split(content)
    chunks: List[str] = []
    buf = ""
    overlap_tail = ""

    def flush_buf():
        nonlocal buf, overlap_tail
        text = buf.strip()
        if text:
            chunks.append(text)
            overlap_tail = text[-OVERLAP_CHARS:] if len(text) > OVERLAP_CHARS else text
        buf = ""

    for p in paras:
        # if paragraph alone is too large, split it further
        if count_tokens(p) > CHUNK_SIZE_TOKENS:
            # flush current buffer first
            if buf.strip():
                flush_buf()
            subparts = split_long_paragraph(p, CHUNK_SIZE_TOKENS, OVERLAP_CHARS)
            for i, sp in enumerate(subparts):
                # prepend overlap from previous chunk if any
                cur = (overlap_tail + sp) if overlap_tail else sp
                # ensure not exceeding token target too much; if it does, just accept
                chunks.append(cur.strip())
                overlap_tail = cur[-OVERLAP_CHARS:] if len(cur) > OVERLAP_CHARS else cur
            continue

        candidate = (buf + "\n\n" if buf else "") + p
        if count_tokens(candidate) >= CHUNK_SIZE_TOKENS:
            # flush current chunk with overlap
            if buf:
                flush_buf()
            # start new chunk with overlap from last
            buf = (overlap_tail + p) if overlap_tail else p
        else:
            buf = candidate

    if buf.strip():
        flush_buf()

    # Prefix each chunk with its heading to keep context
    prefixed = []
    prefix = f"{('#' * level)} {heading}\n\n"
    for c in chunks:
        prefixed.append(prefix + c)
    return prefixed


def build_chunks(md: str) -> List[Dict]:
    sections = split_sections(md)
    out: List[Dict] = []
    chunk_id = 0
    for sec in sections:
        heading = sec["heading"]
        level = sec["level"]
        content = sec["content"]
        anchor = slugify(heading)
        tags = ["agent-context", "ninjamock"] + [t for t in re.split(r"[\s/]+", heading.lower()) if t]
        sec_chunks = chunk_section(heading, level, content)
        for part_index, text in enumerate(sec_chunks):
            out.append({
                "id": f"agent_context-{chunk_id}",
                "section": heading,
                "anchor": anchor,
                "level": level,
                "path": SOURCE_PATH,
                "tags": tags,
                "part_index": part_index,
                "text": text
            })
            chunk_id += 1
    return out


def embed_texts(texts: List[str], model: str = MODEL) -> List[List[float]]:
    embeddings = []
    batch_size = 100
    for i in range(0, len(texts), batch_size):
        resp = openai.embeddings.create(input=texts[i:i+batch_size], model=model)
        embeddings.extend([d.embedding for d in resp.data])
    return embeddings


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def write_jsonl(path: str, rows: List[Dict]):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main():
    ensure_dir(OUT_DIR)
    md = read_markdown(SOURCE_PATH)
    chunks = build_chunks(md)

    # Write JSONL for general pipelines
    write_jsonl(CHUNKS_JSONL_PATH, chunks)

    # Also write metadata.json (array) to be compatible with current rag_search
    with open(METADATA_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    # Build FAISS index
    texts = [c["text"] for c in chunks]
    if not texts:
        raise RuntimeError("No chunks produced from agent_context.md")
    print(f"Embedding {len(texts)} chunks from {SOURCE_PATH}...")
    vectors = embed_texts(texts)
    index = faiss.IndexFlatL2(EMBED_DIM)
    index.add(np.array(vectors).astype("float32"))
    faiss.write_index(index, INDEX_PATH)
    print(f"Wrote index: {INDEX_PATH}\nMetadata JSON: {METADATA_JSON_PATH}\nChunks JSONL: {CHUNKS_JSONL_PATH}")


if __name__ == "__main__":
    main()
