import os
from supabase import create_client
from rag.embeddings import embed_query
from rag.query_transform import transform_query

def get_supabase():
    url, key = os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be configured.")
    return create_client(url, key)

def retrieve(question: str, top_k: int | None = None):
    plan = transform_query(question)
    vector = embed_query(plan.retrieval_query)
    count = top_k or int(os.getenv("RAG_TOP_K", "5"))
    rows = get_supabase().rpc("match_documents", {
        "query_embedding": vector, "match_count": count
    }).execute().data or []
    threshold = float(os.getenv("RAG_MIN_SIMILARITY", "0.35"))
    relevant = [r for r in rows if float(r.get("similarity") or 0) >= threshold]
    diagnostics = {"plan": plan.model_dump(), "top_k": count, "min_similarity": threshold,
                   "retrieved_count": len(rows), "relevant_count": len(relevant)}
    return relevant, diagnostics
