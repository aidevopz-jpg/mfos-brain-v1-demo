import chromadb
from chromadb.config import Settings
from datetime import datetime
from typing import List, Dict, Any

client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="memory_store"
))

COLLECTION_NAME = "mfos_memory"
collection = client.get_or_create_collection(name=COLLECTION_NAME)

def save_memory(text: str, tags: List[str], source_agent: str) -> str:
    id_str = f"mem_{datetime.utcnow().timestamp()}"
    metadata = {
        "tags": tags,
        "created_at": datetime.utcnow().isoformat(),
        "source_agent": source_agent
    }
    collection.add(
        ids=[id_str],
        documents=[text],
        metadatas=[metadata]
    )
    return id_str

def search_memory(query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    items: List[Dict[str, Any]] = []
    if not results["ids"]:
        return items
    for i in range(len(results["ids"][0])):
        items.append({
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
        })
    return items

def list_memory(n_results: int = 50) -> List[Dict[str, Any]]:
    results = collection.get()
    ids = results.get("ids", [])
    docs = results.get("documents", [])
    metas = results.get("metadatas", [])
    items: List[Dict[str, Any]] = []
    for i, id_str in enumerate(ids[:n_results]):
        items.append({
            "id": id_str,
            "text": docs[i],
            "metadata": metas[i],
        })
    return items

def load_initial_memory():
    # Idempotent-ish: only seed if collection is empty
    existing = collection.get()
    if existing.get("ids"):
        return
    examples = [
        (
            "Modernization Score v1\n\nA conceptual description of how MFOS scores buildings based on modernization readiness, risk, and tenant stability.",
            ["modernization", "score", "demo"],
            "Scribe"
        ),
        (
            "PRM Compensation v1\n\nA description of how Portfolio Relationship Managers (PRMs) are compensated in a way that aligns owner outcomes, tenant stability, and vendor dignity.",
            ["PRM", "compensation", "demo"],
            "Scribe"
        ),
        (
            "Vendor Mesh Onboarding v1\n\nA conceptual flow for how vendors are invited, vetted, and onboarded into the MFOS vendor mesh, with emphasis on fairness and reliability.",
            ["vendor", "onboarding", "demo"],
            "Scribe"
        ),
    ]
    for text, tags, source in examples:
        save_memory(text, tags, source)
