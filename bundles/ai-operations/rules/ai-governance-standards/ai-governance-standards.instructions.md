# AI Governance Standards

Controls for LLM and agent workflows in production.

## Risk tiers

- T0: internal drafts with no PII — auto-approve
- T1: customer-facing content — human spot-check
- T2: decisions affecting users — mandatory review
- T3: regulated domains — legal/compliance sign-off

## Evaluation

- Every prompt change runs regression eval set before deploy
- Track latency, cost, and quality metrics per model version
- Log prompts and outputs with retention policy compliance

## Data handling

- No training on customer data without contract permission
- Redact PII before RAG indexing
- Document chunking strategy and retrieval boundaries