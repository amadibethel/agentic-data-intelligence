import os
from openai import OpenAI

def get_openai_client():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is missing.")
    return OpenAI(api_key=key)

def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    response = get_openai_client().embeddings.create(
        model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        input=texts,
        dimensions=int(os.getenv("EMBEDDING_DIMENSIONS", "1536")),
    )
    return [item.embedding for item in response.data]

def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]
