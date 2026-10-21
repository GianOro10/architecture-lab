# High-Level Design: Solution Name

## 1. Executive summary

State the business outcome, scope, and architecture intent.

## 2. Scope

### In scope

- Capability or flow

### Out of scope

- Explicit exclusion

## 3. Drivers and constraints

- Business driver
- Regulatory or security constraint
- Technology constraint

## 4. Architecture context

Identify users, external systems, trust boundaries, and major data flows.

## 5. Logical architecture

Describe components by responsibility, not only by product name.

## 6. Integrations

| Source | Target | Interface | Pattern | Data | SLA |
|---|---|---|---|---|---|
| System A | System B | API/Event/File | Sync/Async | Domain data | Target |

## 7. Data architecture

Define ownership, system of record, lifecycle, retention, lineage, and quality controls.

## 8. Security architecture

Cover identity, authorization, secrets, encryption, audit, privacy, and threat controls.

## 9. Non-functional requirements

| Attribute | Target | Validation |
|---|---|---|
| Availability | Define SLO | Test or evidence |
| Performance | Define latency/throughput | Load test |
| Recovery | Define RTO/RPO | Recovery exercise |

## 10. Observability and operations

Define logs, metrics, traces, alerts, dashboards, runbooks, ownership, and support model.

## 11. Deployment and DevSecOps

Describe environments, CI/CD, quality gates, IaC, rollback, and release governance.

## 12. Risks, assumptions, issues, and dependencies

Track each item with an owner and treatment.

## 13. Architecture decisions

Link the relevant ADRs.
