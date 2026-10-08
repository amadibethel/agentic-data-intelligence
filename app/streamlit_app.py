import os, sys
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")
try:
    for name in ("OPENAI_API_KEY","OPENAI_CHAT_MODEL","OPENAI_EMBEDDING_MODEL","EMBEDDING_DIMENSIONS",
                 "SUPABASE_URL","SUPABASE_KEY","RAG_TOP_K","RAG_MIN_SIMILARITY"):
        if name in st.secrets and not os.getenv(name): os.environ[name] = str(st.secrets[name])
except Exception:
    pass

from rag.retrieval import retrieve
from rag.generation import generate_answer

st.set_page_config(page_title="Klonix Knowledge Intelligence", page_icon="🔎", layout="wide")
st.title("Klonix Knowledge Intelligence Assistant")
st.caption("Grounded RAG · Semantic retrieval · Source traceability")
with st.sidebar:
    st.header("About this demo")
    st.write("Ask about the included synthetic product, policy, and technical-spec records.")
    st.write("Similarity is a retrieval signal, not a factual confidence score.")
    st.metric("Evidence threshold", os.getenv("RAG_MIN_SIMILARITY", "0.35"))
if "messages" not in st.session_state: st.session_state.messages = []
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m.get("sources"):
            with st.expander("Retrieved evidence"):
                for d in m["sources"]:
                    st.markdown(f"**{d.get('document_name')}** · record `{d.get('record_id','n/a')}` · similarity `{float(d.get('similarity') or 0):.3f}`")
                    st.code(d.get("content",""), language="text")
question = st.chat_input("Ask about integrations, support policies, deployment, or technical capabilities…")
if question:
    st.session_state.messages.append({"role":"user","content":question})
    with st.chat_message("user"): st.markdown(question)
    with st.chat_message("assistant"):
        try:
            with st.spinner("Retrieving evidence…"): docs, diagnostics = retrieve(question)
            answer = generate_answer(question, docs)
            st.markdown(answer)
            with st.expander("Retrieval diagnostics"): st.json(diagnostics)
            with st.expander(f"Evidence ({len(docs)} records)"):
                for d in docs:
                    st.markdown(f"**{d.get('document_name')}** · `{d.get('record_id','n/a')}` · similarity `{float(d.get('similarity') or 0):.3f}`")
                    st.code(d.get("content",""), language="text")
            st.session_state.messages.append({"role":"assistant","content":answer,"sources":docs})
        except Exception as exc:
            st.error(f"Request failed: {exc}")
            st.info("Check API keys, Supabase schema, and whether the data has been ingested.")
