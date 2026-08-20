# SRE Standards

Reliability engineering and operational excellence for platform teams.

## Incident response

- Classify severity (SEV1–SEV4) within 5 minutes of page
- Designate incident commander, comms lead, and scribe roles
- Prefer mitigation over root-cause during active incidents

## Blameless culture

- Postmortems focus on systems and process, not individuals
- Action items must have owners and due dates
- Share learnings across teams within 48 hours of closure

## SLO discipline

- Every user-facing service defines SLI, SLO, and error budget
- Alert on burn rate, not every threshold twitch
- Document rollback criteria before every production change

## Security

- Never paste secrets in runbooks or chat; reference vault paths
- Rotate credentials per **secrets-management** skill after incidents