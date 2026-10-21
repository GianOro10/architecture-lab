from uuid import uuid4

from fastapi import FastAPI, HTTPException, Response, status
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

from .config import get_settings
from .models import IngestRequest, IngestResponse, QueryRequest, QueryResponse
from .rag import ExtractiveGenerator, GuardrailViolation, InMemoryDocumentStore, RagService

settings = get_settings()
service = RagService(InMemoryDocumentStore(), ExtractiveGenerator())

REQUESTS = Counter("rag_requests_total", "RAG API requests", ["operation", "outcome"])
QUERY_LATENCY = Histogram("rag_query_duration_seconds", "RAG query latency")

app = FastAPI(
    title="Production RAG Platform Reference",
    version="0.1.0",
    docs_url="/docs" if settings.environment != "production" else None,
)


@app.get("/healthz", tags=["operations"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz", tags=["operations"])
def readiness() -> dict[str, str]:
    return {"status": "ready"}


@app.get("/metrics", include_in_schema=False)
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/v1/documents", response_model=IngestResponse, status_code=status.HTTP_202_ACCEPTED)
def ingest(payload: IngestRequest) -> IngestResponse:
    if any(len(document.text) > settings.max_document_chars for document in payload.documents):
        REQUESTS.labels("ingest", "rejected").inc()
        raise HTTPException(status_code=413, detail="Document exceeds configured character limit")
    accepted = service.ingest(payload.tenant_id, payload.documents)
    REQUESTS.labels("ingest", "accepted").inc()
    return IngestResponse(accepted=accepted, tenant_id=payload.tenant_id)


@app.post("/v1/query", response_model=QueryResponse)
def query(payload: QueryRequest) -> QueryResponse:
    request_id = str(uuid4())
    if len(payload.question) > settings.max_question_chars:
        REQUESTS.labels("query", "rejected").inc()
        raise HTTPException(status_code=413, detail="Question exceeds configured character limit")

    top_k = payload.top_k or settings.default_top_k
    top_k = min(top_k, settings.maximum_top_k)
    try:
        with QUERY_LATENCY.time():
            answer, citations = service.query(payload.tenant_id, payload.question, top_k)
    except GuardrailViolation as exc:
        REQUESTS.labels("query", "rejected").inc()
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    REQUESTS.labels("query", "success").inc()
    return QueryResponse(
        answer=answer,
        citations=citations,
        request_id=request_id,
        grounded=bool(citations),
    )
