# Architecture Review Checklist

## Business and scope

- [ ] Business outcome and measurable success criteria are defined.
- [ ] Scope, exclusions, assumptions, and constraints are explicit.
- [ ] Business capabilities map to solution components.

## Integration and data

- [ ] Systems of record and canonical identifiers are defined.
- [ ] APIs, events, files, and batch flows have contracts and ownership.
- [ ] Idempotency, retries, ordering, reconciliation, and error handling are addressed.
- [ ] Data classification, retention, lineage, and quality rules are defined.

## Security

- [ ] Authentication and authorization follow least privilege.
- [ ] Secrets and keys use an approved lifecycle.
- [ ] Encryption, auditability, privacy, and threat scenarios are covered.
- [ ] Dependencies and build artifacts are scanned.

## Reliability and operations

- [ ] Availability, latency, capacity, RTO, and RPO are measurable.
- [ ] Failure modes, timeouts, circuit breakers, and recovery paths are documented.
- [ ] Logs, metrics, traces, alerts, dashboards, and SLOs are defined.
- [ ] Runbooks, support ownership, escalation, and cost accountability exist.

## Delivery and governance

- [ ] CI/CD quality gates and Infrastructure as Code are defined.
- [ ] Environments, configuration, rollback, and release strategy are documented.
- [ ] ADRs capture material decisions and trade-offs.
- [ ] Risks, dependencies, and technical debt have owners and treatment dates.
