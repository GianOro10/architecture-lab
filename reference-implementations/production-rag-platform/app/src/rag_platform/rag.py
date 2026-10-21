import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Protocol

from .models import Citation, Document

TOKEN_PATTERN = re.compile(r"[\w-]+", re.UNICODE)
INJECTION_PATTERNS = (
    re.compile(r"ignore (all |any )?(previous|prior) instructions", re.IGNORECASE),
    re.compile(r"reveal (the )?(system|developer) prompt", re.IGNORECASE),
)


class GuardrailViolation(ValueError):
    """Raised when an input violates an explicit safety rule."""


@dataclass(frozen=True)
class SearchHit:
    document: Document
    score: float


class DocumentStore(Protocol):
    def add(self, tenant_id: str, documents: list[Document]) -> int: ...

    def search(self, tenant_id: str, query: str, top_k: int) -> list[SearchHit]: ...


class Generator(Protocol):
    def generate(self, question: str, hits: list[SearchHit]) -> str: ...


def _tokens(text: str) -> set[str]:
    return {token.lower() for token in TOKEN_PATTERN.findall(text) if len(token) > 1}


class InMemoryDocumentStore:
    """Deterministic adapter used for local execution and contract tests."""

    def __init__(self) -> None:
        self._documents: dict[str, dict[str, Document]] = defaultdict(dict)

    def add(self, tenant_id: str, documents: list[Document]) -> int:
        for document in documents:
            self._documents[tenant_id][document.id] = document
        return len(documents)

    def search(self, tenant_id: str, query: str, top_k: int) -> list[SearchHit]:
        query_tokens = _tokens(query)
        ranked: list[SearchHit] = []
        for document in self._documents.get(tenant_id, {}).values():
            document_tokens = _tokens(document.text)
            union = query_tokens | document_tokens
            score = len(query_tokens & document_tokens) / len(union) if union else 0.0
            if score > 0:
                ranked.append(SearchHit(document=document, score=score))
        return sorted(ranked, key=lambda hit: hit.score, reverse=True)[:top_k]


class ExtractiveGenerator:
    """Grounded local generator; replace through the Generator port in production."""

    def generate(self, question: str, hits: list[SearchHit]) -> str:
        del question
        if not hits:
            return "I do not have enough grounded context to answer this question."
        excerpts = [hit.document.text.strip()[:500] for hit in hits]
        return "Based on the indexed sources: " + " ".join(excerpts)


class RagService:
    def __init__(self, store: DocumentStore, generator: Generator) -> None:
        self._store = store
        self._generator = generator

    @staticmethod
    def validate_question(question: str) -> None:
        if any(pattern.search(question) for pattern in INJECTION_PATTERNS):
            raise GuardrailViolation("Question rejected by prompt-injection guardrail")

    def ingest(self, tenant_id: str, documents: list[Document]) -> int:
        return self._store.add(tenant_id, documents)

    def query(self, tenant_id: str, question: str, top_k: int) -> tuple[str, list[Citation]]:
        self.validate_question(question)
        hits = self._store.search(tenant_id, question, top_k)
        citations = [
            Citation(
                document_id=hit.document.id,
                source=hit.document.source,
                score=round(hit.score, 4),
            )
            for hit in hits
        ]
        return self._generator.generate(question, hits), citations
