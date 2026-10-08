import re
from rag.schemas import QueryPlan

ATTRIBUTE_TERMS = {
    "integration": ["integration", "integrate", "connect", "works with", "supports"],
    "support": ["support", "sla", "response time", "service level"],
    "deployment": ["deployment", "deploy", "hosting", "cloud", "on-prem"],
    "security": ["security", "authentication", "auth", "oauth"],
    "availability": ["available", "availability", "status"],
    "pricing": ["price", "pricing", "cost", "fee"],
}

def transform_query(question: str) -> QueryPlan:
    cleaned = re.sub(r"\\s+", " ", question).strip()
    lower = cleaned.lower()
    attrs = [key for key, terms in ATTRIBUTE_TERMS.items()
             if any(term in lower for term in terms)]
    intent = "comparison" if any(x in lower for x in ("compare", "better", "difference")) else (
        "lookup" if any(x in lower for x in ("which", "what", "who", "when")) else "general")
    expanded = cleaned + ((" " + " ".join(attrs)) if attrs else "")
    return QueryPlan(original_question=cleaned, retrieval_query=expanded, intent=intent, attributes=attrs)
