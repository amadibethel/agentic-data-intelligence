from pydantic import BaseModel, Field

class QueryPlan(BaseModel):
    original_question: str
    retrieval_query: str
    intent: str = "general"
    entities: list[str] = Field(default_factory=list)
    attributes: list[str] = Field(default_factory=list)
