import json, os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from rag.embeddings import embed_texts
from rag.retrieval import get_supabase

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

def record_to_text(record: dict) -> str:
    return "\\n".join(f"{k.replace('_',' ').title()}: {v if v not in (None, '') else 'Not specified'}"
                       for k, v in record.items())

def load_records():
    rows = []
    for path in sorted(DATA_DIR.glob("*.csv")):
        for i, record in enumerate(pd.read_csv(path).fillna("").to_dict(orient="records"), 1):
            rows.append({"document_name":path.name, "document_type":"csv",
                         "record_id":str(record.get("product_id") or record.get("policy_id") or i),
                         "content":record_to_text(record), "metadata":{"record":record}})
    for path in sorted(DATA_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict): data = data.get("records", [data])
        if not isinstance(data, list): raise ValueError(f"{path.name} must be a JSON list")
        for i, record in enumerate(data, 1):
            rows.append({"document_name":path.name, "document_type":"json",
                         "record_id":str(record.get("product_id") or record.get("product_name") or i),
                         "content":record_to_text(record), "metadata":{"record":record}})
    return rows

def ingest():
    load_dotenv(ROOT / ".env")
    rows = load_records()
    client = get_supabase()
    for start in range(0, len(rows), 64):
        batch = rows[start:start+64]
        vectors = embed_texts([r["content"] for r in batch])
        payload = [{**r, "embedding":v} for r,v in zip(batch,vectors)]
        client.table("documents").upsert(payload, on_conflict="document_name,record_id").execute()
        print(f"Ingested {min(start+len(batch),len(rows))}/{len(rows)}")
    return len(rows)

if __name__ == "__main__":
    print(f"Finished: {ingest()} records")
