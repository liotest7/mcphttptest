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
EMBED_DIM = 1536

UI_TEMPLATES_PATH = "data/ui_templates.json"
INDEX_DIR = "indices/ui_templates/"
INDEX_PATH = os.path.join(INDEX_DIR, "faiss_index.index")
METADATA_PATH = os.path.join(INDEX_DIR, "metadata.json")

def load_ui_templates(json_file=UI_TEMPLATES_PATH):
    with open(json_file, "r", encoding="utf-8") as file:
        return json.load(file)

def flatten_properties(props, prefix=""):  # Recursively flatten nested properties
    items = []
    for k, v in props.items():
        key = f"{prefix}{k}" if prefix else k
        if isinstance(v, dict):
            items.extend(flatten_properties(v, prefix=key+"."))
        else:
            items.append(f"{key}: {v}")
    return items

def template_to_text(template):
    title = template.get("title", "")
    type_ = template.get("type", "")
    category = template.get("category", "")
    template_id = template.get("templateId", "")
    description = template.get("description", "") or ""
    author = template.get("author", "")
    tags = ", ".join(template.get("tags", []))
    properties = template.get("properties", {})
    children = template.get("children", {})
    default_properties = template.get("defaultProperties", {})
    # Flatten properties and children
    prop_str = ", ".join(flatten_properties(properties))
    child_str = ""
    if isinstance(children, dict) and children:
        child_str = ", ".join(flatten_properties(children.get("properties", {}), prefix="child."))
    elif isinstance(children, list):
        for idx, child in enumerate(children):
            child_str += ", ".join(flatten_properties(child.get("properties", {}), prefix=f"child{idx}.")) + ", "
    default_prop_str = ", ".join(flatten_properties(default_properties, prefix="default."))
    return f"UI Template: {title}\nType: {type_}\nCategory: {category}\nTemplateId: {template_id}\nDescription: {description}\nAuthor: {author}\nTags: {tags}\nProperties: {prop_str}\n{child_str}\nDefaultProperties: {default_prop_str}"

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

def build_ui_templates_index(templates):
    all_texts = []
    metadata = []
    for template in templates:
        text = template_to_text(template)
        all_texts.append(text)
        metadata.append({
            "id": template.get("id"),
            "title": template.get("title"),
            "type": template.get("type"),
            "category": template.get("category"),
            "templateId": template.get("templateId"),
            "author": template.get("author"),
            "tags": template.get("tags", []),
            "properties": template.get("properties", {}),
            "children": template.get("children", {}),
            "defaultProperties": template.get("defaultProperties", {}),
            "text": text
        })
    print(f"Total templates: {len(all_texts)}")
    print("Embedding templates...")
    embeddings = embed_text(all_texts)
    print("Creating FAISS index...")
    index = faiss.IndexFlatL2(EMBED_DIM)
    index.add(np.array(embeddings).astype('float32'))
    faiss.write_index(index, INDEX_PATH)
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)
    print(f"Index and metadata saved in {INDEX_DIR}")

if __name__ == "__main__":
    templates = load_ui_templates()
    build_ui_templates_index(templates)
    print("UI templates indexing completed.")
