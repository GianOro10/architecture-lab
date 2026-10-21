from pydantic import BaseModel, Field


class Document(BaseModel):
    id: str = Field(min_length=1, max_length=128)
    text: str = Field(min_length=1)
    source: str = Field(min_length=1, max_length=512)


class IngestRequest(BaseModel):
    tenant_id: str = Field(pattern=r"^[a-zA-Z0-9_-]{1,64}$")
    documents: list[Document] = Field(min_length=1, max_length=100)


class IngestResponse(BaseModel):
    accepted: int
    tenant_id: str


class QueryRequest(BaseModel):
    tenant_id: str = Field(pattern=r"^[a-zA-Z0-9_-]{1,64}$")
    question: str = Field(min_length=3)
    top_k: int | None = Field(default=None, ge=1, le=10)


class Citation(BaseModel):
    document_id: str
    source: str
    score: float


class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation]
    request_id: str
    grounded: bool
