# ADR-0002: Select Synchronous, Asynchronous, or Hybrid Integration

- **Status:** Accepted
- **Date:** 2026-10-21
- **Decision owners:** Architecture Lab

## Context

Enterprise solutions frequently default to REST APIs or messaging based on team preference instead of business behavior and non-functional requirements. This creates avoidable coupling, latency, retry storms, data inconsistency, and operational ambiguity.

A repeatable decision framework is required to select the interaction model for each business flow.

## Decision

The integration pattern will be selected from the business interaction and its quality attributes:

| Criterion | Synchronous API | Asynchronous event/message | Hybrid |
|---|---|---|---|
| Immediate response required | Preferred | Not preferred | Command response plus later events |
| Temporal coupling acceptable | Required | Not required | Limited |
| Traffic bursts expected | Risk of saturation | Preferred with buffering | Preferred when acknowledgement is enough |
| Long-running process | Not preferred | Preferred | Preferred |
| Replay or multiple consumers | Limited | Preferred | Preferred |
| Strong request-level consistency | Preferred | Requires explicit design | Depends on boundary |
| Failure isolation | Lower | Higher | Higher with added complexity |

### Selection rules

1. Use a **synchronous API** when the consumer needs an immediate outcome, the operation is short-lived, and both parties can meet the same availability and latency expectations.
2. Use an **asynchronous event or message** when producers and consumers must be decoupled, workloads are bursty, processing is long-running, or replay and multiple consumers are expected.
3. Use a **hybrid pattern** when the caller needs immediate acknowledgement but the business outcome completes asynchronously.
4. Do not use asynchronous processing to hide an undefined consistency model.
5. Do not create event chains without explicit ownership, correlation, timeout, and recovery behavior.

## Required architecture controls

### Contracts and compatibility

- Version APIs and event schemas using an explicit compatibility policy.
- Define mandatory, optional, and deprecated fields.
- Validate contracts in CI/CD.
- Assign an owner and lifecycle to every interface.

### Reliability

- Define idempotency keys for retried commands and messages.
- Specify retry limits, backoff, timeout, dead-letter handling, and reconciliation.
- Document ordering and duplicate-delivery expectations.
- Use transactional outbox or an equivalent consistency mechanism when state changes and event publication must remain aligned.

### Observability

- Propagate correlation and trace identifiers across all hops.
- Measure latency, throughput, error rate, retry volume, queue age, and dead-letter volume.
- Define alerts from service-level objectives, not only infrastructure thresholds.
- Provide operational dashboards and runbooks with named ownership.

### Security

- Apply least privilege to APIs, topics, queues, and service identities.
- Protect data in transit and at rest.
- Avoid placing secrets or unnecessary sensitive information in events.
- Retain audit evidence according to data classification and regulatory needs.

## Consequences

### Positive

- Integration choices are tied to measurable requirements.
- Failure isolation, scalability, and recovery become explicit.
- Teams use consistent language for architecture reviews.
- Operational controls are defined before implementation.

### Trade-offs

- Asynchronous flows introduce eventual consistency and operational complexity.
- Hybrid designs require clear separation between acknowledgement and business completion.
- Contract governance and observability require continuous ownership.
- Additional infrastructure is justified only when the flow benefits from decoupling.

## Alternatives considered

### REST for every interaction

Rejected because it creates temporal coupling and performs poorly for long-running, bursty, or fan-out workloads.

### Messaging for every interaction

Rejected because it adds unnecessary complexity when an immediate response and simple consistency boundary are required.

### Team-by-team selection without shared criteria

Rejected because it produces inconsistent decisions, duplicated controls, and difficult operations.

## Validation

For each integration, the HLD must record:

- Selected interaction pattern and rationale
- Expected latency and throughput
- Availability and recovery targets
- Consistency and delivery semantics
- Retry, timeout, dead-letter, and reconciliation behavior
- Security classification and access model
- Observability signals, dashboard, runbook, and owner
