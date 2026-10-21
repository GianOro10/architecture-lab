# Runbook: RAG query degradation

## Trigger

- Query error rate above 5% for 10 minutes.
- Query p95 above 2 seconds for 10 minutes.
- No successful queries for 15 minutes.

## Triage

1. Confirm impact by tenant, region and API version.
2. Correlate the alert with deployment, configuration and provider changes.
3. Inspect request traces to separate retrieval latency from generation latency.
4. Check vector-store saturation, managed-model quotas and network errors.
5. Validate that the grounded no-result path is not being counted as a failure.

## Mitigation

1. Stop or roll back the latest deployment when correlation is strong.
2. Reduce `top_k` within the approved quality envelope if retrieval is saturated.
3. Activate the approved secondary model or region when a provider is impaired.
4. Preserve the rule that no context means no generated answer.

## Verification

- Error rate remains below 1% for 30 minutes.
- p95 returns below the service objective.
- Evaluation samples remain above the approved groundedness threshold.
- No cross-tenant retrieval is observed.

## Escalation evidence

Attach request IDs, trace IDs, affected tenants, timestamps, deployment SHA, provider status and mitigation performed. Never attach prompts or retrieved documents containing sensitive data to an unrestricted incident channel.

## Rollback

Redeploy the last signed immutable image digest and restore the previous configuration revision. Do not roll back indexes without confirming schema compatibility and backup freshness.
