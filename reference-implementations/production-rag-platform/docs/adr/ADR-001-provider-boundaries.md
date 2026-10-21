# ADR-001: Isolate model and vector-store providers behind ports

- Status: Accepted
- Date: 2026-10-21

## Context

Embedding models, vector databases and generation models have different data residency, cost, latency, availability and lock-in profiles. Binding the HTTP contract directly to one provider makes later migration expensive and complicates testing.

## Decision

The application core depends on `DocumentStore` and `Generator` protocols. Provider SDKs belong in adapters. The default repository adapter is deterministic, local and credential-free; it exists for contract testing, not as a production vector database.

Provider adapters must preserve:

- tenant filtering in every retrieval operation;
- ranked results with stable document identifiers and sources;
- request timeouts, bounded retries and circuit breaking;
- trace propagation and token/cost metrics;
- an explicit no-result response instead of ungrounded generation.

## Consequences

### Positive

- Provider changes do not alter the API contract.
- Tests run without cloud credentials or paid model calls.
- Multi-region and data-residency strategies remain possible.

### Negative

- Adapters require contract tests and operational ownership.
- Provider-specific capabilities must not leak into the domain boundary.

## Alternatives rejected

- Direct provider SDK calls from API handlers: lower initial effort but high coupling.
- A universal abstraction framework as the domain: fast prototyping but transfers control of core contracts to a dependency.
