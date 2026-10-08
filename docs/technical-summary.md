# Technical Summary

## Part 1 — RAG
CSV rows and JSON objects are ingested as individual records, rendered into readable text, tagged with source filename/record ID, embedded, and stored in Supabase pgvector. At query time, a lightweight query transformer expands attributes, semantic retrieval selects nearest records, and the generation prompt restricts answers to supplied evidence. The UI exposes retrieved records and similarity scores.

## Part 2 — Agent
The intended flow is Google Calendar + Gmail → structured extraction → normalization → deduplication → web evidence → deterministic scoring → CSV/database/report. The n8n export is a configurable template; credentials and node-output mappings must be selected and tested in the target instance. Python modules provide reusable normalization, deduplication, verification, and CSV export.

## Principles
Separate extraction from validation; preserve provenance and contradictions; use deterministic rules for schema, email syntax and deduplication; missing evidence is unknown rather than false; escalate conflicting claims; keep credentials server-side.

## Limitations
Embedding similarity does not prove truth; data is synthetic and small; score is heuristic; web snippets can be incomplete; identity ambiguity requires human review; n8n provider schemas vary.
