# ADR-0003: Decouple the RAG Platform from the LLM Provider

- **Status:** Proposed
- **Date:** 2026-10-26
- **Decision owners:** Architecture Lab

## Context

The production RAG reference implementation needs to evolve without coupling retrieval, grounding, citations, guardrails, and observability to one LLM vendor or model.

Direct use of a provider SDK inside the application core would make model replacement faster initially, but it would spread provider-specific request formats, response fields, error handling, and telemetry across the service. A universal gateway could centralize those concerns, but it would add infrastructure and operational ownership before the reference implementation needs them.

The design must preserve these quality attributes:

- Grounded answers and citations remain part of the application contract.
- Provider credentials never enter application logs or responses.
- Provider and model changes are configuration-driven.
- Failures are explicit and observable; silent semantic degradation is not acceptable.
- Local and CI tests do not require paid external model calls.

## Decision

Introduce a thin provider adapter at the application boundary.

The application core will depend on an internal `LLMProvider` contract rather than a vendor SDK. The contract will accept the normalized prompt, retrieved context, generation parameters, correlation identifier, and timeout. It will return normalized answer content, token usage when available, finish reason, provider, model, and latency metadata.

Provider-specific SDKs, authentication, request mapping, response normalization, retry classification, and error translation will remain inside adapter implementations.

One provider and model will be active for each deployment through validated configuration. Changing the provider requires an explicit configuration change and deployment.

Automatic cross-provider failover will not be implemented initially. Different models can produce materially different answers, citations, safety behavior, latency, and cost. A provider outage will therefore fail clearly according to the service error contract instead of silently switching models.

## Required architecture controls

### Contract and boundaries

- Keep retrieval, citation construction, and grounding validation outside provider adapters.
- Prevent provider-specific types from crossing into the application core.
- Use stable internal error categories: timeout, rate limited, unavailable, invalid response, authentication failure, and policy rejection.
- Reject startup when required provider configuration or secrets are missing.

### Reliability and cost

- Apply explicit request timeouts and bounded retries only to failures classified as transient.
- Do not retry authentication, policy, or invalid-response failures automatically.
- Record token usage and estimated cost when the provider exposes sufficient data.
- Protect the service with concurrency and token-budget limits.

### Security

- Load credentials from the deployment secret mechanism, never from committed files.
- Redact prompts, retrieved content, credentials, and sensitive response data from default logs.
- Allow payload capture only through an explicit, access-controlled diagnostic mode.

### Observability

Emit provider-neutral telemetry with low-cardinality attributes:

- `llm.provider`
- `llm.model`
- `llm.operation`
- `llm.outcome`
- latency
- input and output token counts when available

Do not use prompt text, user identifiers, or correlation identifiers as metric labels.

## Consequences

### Positive

- The RAG core remains portable across providers and models.
- Provider changes are isolated to adapters and configuration.
- Tests can use a deterministic fake adapter without network access or usage cost.
- Security, reliability, and telemetry controls remain consistent.
- Provider comparison can be performed against the same application contract.

### Trade-offs

- The internal contract must be maintained as provider capabilities evolve.
- Some provider-specific features may require optional adapter extensions or remain unavailable.
- Response normalization can hide useful differences if the contract grows too broad.
- Explicit provider switching does not provide automatic continuity during an outage.
- Each adapter adds contract, integration, and operational testing effort.

## Alternatives considered

### Use a provider SDK directly in the application core

Rejected because it couples business logic, error handling, telemetry, and tests to one vendor.

### Introduce a universal LLM gateway now

Deferred because it adds another runtime component, availability dependency, security boundary, and operating cost. It can be reconsidered when multiple production providers or centralized policy enforcement justify it.

### Implement automatic cross-provider failover

Rejected for the initial design because equivalent prompts do not guarantee equivalent grounding, safety, latency, token usage, or output quality across models. Failover requires evaluation evidence and explicit acceptance criteria.

### Self-host the model

Deferred because model serving, accelerator capacity, patching, scaling, and evaluation would materially expand the scope of this reference implementation.

## Validation

The decision is validated when:

1. The application core imports only the internal `LLMProvider` contract.
2. A deterministic fake adapter supports unit and CI tests without external calls.
3. The production adapter passes contract tests for success, timeout, rate limit, invalid response, and unavailable scenarios.
4. Configuration validation prevents startup with an unknown provider or missing model.
5. Traces and metrics identify provider, model, latency, outcome, and token usage without exposing prompts or secrets.
6. A controlled provider change requires no modification to retrieval, citation, or grounding logic.

Automatic failover may be reconsidered in a superseding ADR after two providers pass the same quality, safety, latency, and cost evaluation suite.
