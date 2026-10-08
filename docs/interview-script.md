# 25-minute walkthrough

**0–2 min:** Explain the goal: evidence-grounded answers plus a reviewable data-verification workflow.

**2–5 min:** Show architecture and separation between retrieval, LLM reasoning, tools, and deterministic checks.

**5–10 min:** Ask the RAG app: “Which products integrate with Paystack?”, “Which Paystack-enabled product has priority support?”, and an unsupported cryptocurrency-withdrawal question. Expand source evidence.

**10–14 min:** Explain record-level ingestion, embeddings, pgvector, query transformation, context construction, and citations.

**14–20 min:** Run n8n using synthetic test data. Show extraction, normalization, deduplication, web evidence mapping, scoring, and output.

**20–23 min:** Discuss why deterministic checks handle deduplication/validation and why contradictions go to human review.

**23–25 min:** Future work: hybrid search, reranking, evaluation, observability, source reliability, audit logs, and calibrated confidence.

Closing: “Generated text is not treated as truth. Evidence, deterministic validation, and explicit uncertainty control what the system concludes.”
