# Architecture Lab

[![Architecture Quality](https://github.com/GianOro10/architecture-lab/actions/workflows/architecture-quality.yml/badge.svg)](https://github.com/GianOro10/architecture-lab/actions/workflows/architecture-quality.yml)
[![Production RAG Quality](https://github.com/GianOro10/architecture-lab/actions/workflows/reference-implementation-quality.yml/badge.svg)](https://github.com/GianOro10/architecture-lab/actions/workflows/reference-implementation-quality.yml)

A practical, vendor-neutral collection of enterprise architecture patterns, Architecture Decision Records (ADRs), High-Level Design (HLD) templates, and review checklists.

## Focus areas

| Domain | Topics |
|---|---|
| Enterprise architecture | Capabilities, AS-IS / TO-BE, roadmaps, governance |
| Integration | API-first, events, messaging, data flows, contracts |
| Cloud platforms | Resilience, scalability, landing zones, cost awareness |
| DevSecOps | CI/CD, quality gates, supply-chain security, IaC |
| Observability | Logs, metrics, traces, SLOs, operational readiness |
| Applied AI/LLM | Architecture analysis, documentation, guardrails, automation |

## Repository map

- `docs/adr/` — real architecture decisions and trade-offs
- `docs/hld/` — complete reference solution designs with Mermaid diagrams
- `docs/templates/` — reusable ADR and HLD templates
- `checklists/` — practical architecture review controls
- `scripts/` — documentation quality validation
- `reference-implementations/` — executable architecture examples with tests and delivery controls
- `.github/workflows/` — automated quality checks

## Working cadence

The repository evolves through small, reviewable improvements. Each change must add professional value: a decision, pattern, checklist control, example, or automation improvement.

## Quality principles

1. State context, assumptions, constraints, and trade-offs.
2. Separate business, application, data, integration, security, and operations concerns.
3. Define NFRs with measurable targets.
4. Include observability, resilience, security, and ownership by design.
5. Keep examples generic and free of confidential or proprietary information.

## Featured reference architecture

- [Production RAG Platform Reference](reference-implementations/production-rag-platform/) — executable FastAPI service with grounded responses and citations, Terraform for AWS, hardened Kubernetes, OpenTelemetry, SLO alerts, security controls, tests, and CI.
- [Cloud-Native Integration Platform HLD](docs/hld/cloud-native-integration-platform.md) — APIs, events, security, reliability, observability, NFRs, DevSecOps, and three Mermaid diagrams.
- [Integration Pattern Selection ADR](docs/adr/ADR-0002-integration-pattern-selection.md) — decision framework for synchronous, asynchronous, and hybrid integration.

## Current roadmap

- Add an automated RAG evaluation dataset and quality thresholds.
- Add GitOps promotion and signed container provenance.
- Add a second cloud deployment mapping to demonstrate portability trade-offs.

## Author

**Giussepe Gianniny Hernández Oropeza**  
Senior Solutions Architect — Enterprise Architecture · Cloud · DevSecOps · Integration · AI/LLM

[LinkedIn](https://mx.linkedin.com/in/giussepe-gianniny-hdz-o)
