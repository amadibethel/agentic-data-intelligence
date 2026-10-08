# Agentic Data Intelligence & Verification Platform

Two connected demos:
1. **Klonix Knowledge Intelligence Assistant** — Streamlit RAG over CSV/JSON records, OpenAI embeddings, Supabase pgvector, source traceability.
2. **Meeting Intelligence & Attendee Verification Agent** — n8n template plus reusable Python normalization, deduplication, verification and CSV export modules.

## Quick start
Python 3.10+ recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Configure `.env`, run `sql/schema.sql` in Supabase SQL Editor, then:

```bash
python -m rag.ingestion
streamlit run app/streamlit_app.py
python -m unittest discover -s tests -v
python -m agent.demo
```

Deploy Streamlit Community Cloud using `app/streamlit_app.py` as the entry point. Add secrets in the hosting dashboard; never commit credentials.

## Part 2 / n8n
Import `n8n/meeting-verification-agent.json`, select credentials in your instance, configure the search provider, and adapt provider-specific output mappings. The export is a **template**, not a tested turnkey integration: n8n node versions, OAuth credentials, scopes, and provider response shapes vary. Test using synthetic data and a dedicated calendar/email account.

## Important
Data is synthetic. Verification scores are heuristic, not calibrated probabilities. Missing evidence is not proof a claim is false. Preserve provenance and escalate conflicts. Do not process real attendee personal data without authorization.
