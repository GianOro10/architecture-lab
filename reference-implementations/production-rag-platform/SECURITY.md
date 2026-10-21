# Security policy

## Supported version

Only the latest commit on `main` is maintained in this reference repository.

## Reporting

Do not open a public issue containing credentials, exploitable details or sensitive data. Use GitHub private vulnerability reporting when enabled for the repository owner.

## Threat boundaries

- User input and retrieved documents are untrusted.
- Tenant identity must come from a verified token at the gateway, not from an arbitrary request body in a production adapter.
- Model output is untrusted and must be encoded or validated by its downstream consumer.
- Secrets must be injected from a managed secret store and rotated outside the image.
- Production egress must use explicit destinations; the sample RFC1918 policy is a placeholder that must be narrowed.

## Required production controls

- OIDC/OAuth 2.0 authentication and policy-based authorization.
- Private networking for data and model providers where supported.
- SAST, SCA, secret scanning, image scanning and signed provenance.
- Encryption in transit and at rest with auditable key rotation.
- Prompt, document and output data-classification policy.
- Backup restore tests and regional recovery exercises.
- RAG evaluation for groundedness, retrieval quality, harmful output and leakage.
