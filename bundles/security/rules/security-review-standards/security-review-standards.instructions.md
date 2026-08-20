# Security Review Standards

Risk-based application security assessments.

## Scope

- Classify asset criticality and data sensitivity before review depth
- Threat model for new features handling auth, payments, or PII
- Map findings to CWE/OWASP categories

## Severity

- Critical: exploitable without auth or data exfiltration — block release
- High: exploitable with low complexity — fix before GA
- Medium/Low: track in backlog with SLA

## Reporting

- Provide reproduction steps and remediation guidance
- Never include live exploit payloads in tickets
- Escalate suspected active compromise immediately