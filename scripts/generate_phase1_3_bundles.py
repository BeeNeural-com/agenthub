#!/usr/bin/env python3
"""Generate Phase 1-3 department bundles from catalog Appendix A."""
from __future__ import annotations

import textwrap
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

BUNDLES: dict = {
    "document-processing": {
        "name": "Document Processing",
        "description": "Create, analyze, and transform office documents (Word, Excel, PowerPoint, PDF) for cross-department workflows.",
        "tags": ["documents", "docx", "xlsx", "pptx", "pdf"],
        "skills": ["docx-authoring", "xlsx-analysis", "pptx-generation", "pdf-extraction"],
        "agent": None,
        "rule": ("document-standards", "Document Standards", "Formatting, accessibility, and version control for office deliverables."),
        "prompt": ("kickoff-document", "Kickoff Document Task", "Start a structured document authoring or analysis thread."),
    },
    "product-management": {
        "name": "Product Management",
        "description": "Discovery, PRDs, roadmaps, prioritization, and sprint planning for product teams.",
        "tags": ["product", "prd", "roadmap", "discovery"],
        "skills": [
            "prd-writer", "feature-spec", "roadmap-builder", "feature-prioritization",
            "user-research-synthesis", "product-discovery", "sprint-planning",
        ],
        "agent": ("product-manager", "Product Manager", "product"),
        "rule": ("product-methodology", "Product Methodology", "Outcome-driven product development standards."),
        "prompt": ("kickoff-product", "Kickoff Product Work", "Classify product request and propose discovery or delivery plan."),
    },
    "devops-sre": {
        "name": "DevOps & SRE",
        "description": "CI/CD, deployments, incidents, SLOs, monitoring, and secrets management for platform reliability.",
        "tags": ["devops", "sre", "ci-cd", "incident", "observability"],
        "skills": [
            "ci-cd-pipeline", "deployment-strategy", "incident-response-runbook",
            "incident-postmortem", "slo-sli-tracking", "monitoring-setup", "secrets-management",
        ],
        "agent": ("devops-engineer", "DevOps Engineer", "devops"),
        "rule": ("sre-standards", "SRE Standards", "Reliability, blameless culture, and operational excellence."),
        "prompt": ("kickoff-incident", "Kickoff Incident Response", "Triage incident severity and propose runbook steps."),
    },
    "software-engineering-general": {
        "name": "Software Engineering (General)",
        "description": "Language-agnostic engineering workflows: review, TDD, architecture, APIs, RFCs, and changelogs.",
        "tags": ["software-engineering", "architecture", "testing", "api"],
        "skills": [
            "code-review", "test-driven-development", "testing-strategy", "system-design",
            "software-architecture", "api-design", "changelog-generator", "technical-rfc",
        ],
        "agent": None,
        "rule": ("engineering-standards", "General Engineering Standards", "Code quality, design review, and documentation norms."),
        "prompt": None,
    },
    "ai-operations": {
        "name": "AI Operations",
        "description": "Prompt engineering, RAG pipelines, LLM risk review, and multi-agent workflow design.",
        "tags": ["ai", "llm", "rag", "prompts", "mlops"],
        "skills": [
            "prompt-engineering", "prompt-evaluation", "rag-pipeline-design",
            "llm-risk-review", "agent-workflow-design",
        ],
        "agent": ("ml-engineer", "ML Engineer", "ai-operations"),
        "rule": ("ai-governance-standards", "AI Governance Standards", "Safety tiers, eval gates, and production AI controls."),
        "prompt": ("kickoff-ai-workflow", "Kickoff AI Workflow", "Design or review an LLM/agent workflow with eval plan."),
    },
    "data-analytics": {
        "name": "Data & Analytics",
        "description": "SQL review, exploration, statistics, dashboards, and KPI definition for data-driven decisions.",
        "tags": ["data", "analytics", "sql", "kpi", "dashboard"],
        "skills": [
            "sql-query-review", "data-exploration", "statistical-analysis",
            "dashboard-design", "kpi-definition",
        ],
        "agent": ("data-analyst", "Data Analyst", "data-analytics"),
        "rule": ("data-quality-standards", "Data Quality Standards", "Reproducible analysis, metric definitions, and chart integrity."),
        "prompt": ("kickoff-analysis", "Kickoff Data Analysis", "Scope an analytics question and select skills."),
    },
    "security": {
        "name": "Security",
        "description": "Threat modeling, OWASP review, secrets scanning, and vulnerability triage for application security.",
        "tags": ["security", "appsec", "owasp", "threat-model"],
        "skills": ["threat-modeling", "owasp-top10-review", "secrets-scanning", "vulnerability-triage"],
        "agent": None,
        "rule": ("security-review-standards", "Security Review Standards", "Risk-based security assessment methodology."),
        "prompt": ("kickoff-security-review", "Kickoff Security Review", "Classify security request and select review depth."),
    },
    "marketing": {
        "name": "Marketing & Growth",
        "description": "Campaign planning, content, SEO, email, and landing page copy for go-to-market teams.",
        "tags": ["marketing", "campaign", "seo", "content"],
        "skills": [
            "campaign-plan", "content-marketing", "seo-audit", "seo-content-optimization",
            "email-marketing", "landing-page-copy",
        ],
        "agent": ("marketing-manager", "Marketing Manager", "marketing"),
        "rule": ("marketing-standards", "Marketing Standards", "Brand voice, compliance, and measurable campaign goals."),
        "prompt": ("kickoff-campaign", "Kickoff Marketing Campaign", "Define campaign objective, audience, and channel plan."),
    },
    "sales": {
        "name": "Sales & Revenue",
        "description": "Discovery prep, account research, outreach, battlecards, and lead qualification.",
        "tags": ["sales", "revenue", "outreach", "discovery"],
        "skills": [
            "discovery-call-prep", "account-research", "call-prep", "draft-outreach",
            "competitive-battlecard", "lead-qualification",
        ],
        "agent": ("account-executive", "Account Executive", "sales"),
        "rule": ("sales-methodology", "Sales Methodology", "Discovery-first selling and CRM hygiene."),
        "prompt": ("kickoff-deal", "Kickoff Deal Prep", "Prepare for account meeting or outreach sequence."),
    },
    "customer-success": {
        "name": "Customer Success",
        "description": "Support triage, KB articles, QBR prep, and churn analysis for customer retention.",
        "tags": ["customer-success", "support", "qbr", "churn"],
        "skills": [
            "ticket-triage", "support-response-draft", "kb-article-writer",
            "qbr-prep", "churn-analysis",
        ],
        "agent": ("customer-success-manager", "Customer Success Manager", "customer-success"),
        "rule": ("customer-success-standards", "Customer Success Standards", "Empathy, SLA alignment, and health scoring."),
        "prompt": ("kickoff-qbr", "Kickoff QBR Prep", "Plan quarterly business review with customer context."),
    },
    "finance": {
        "name": "Finance & FP&A",
        "description": "Budgeting, forecasting, variance analysis, and unit economics with governance disclaimers.",
        "tags": ["finance", "fp-and-a", "budget", "forecast"],
        "skills": ["budget-plan", "financial-forecast", "variance-analysis", "unit-economics"],
        "agent": ("fp-and-a-analyst", "FP&A Analyst", "finance"),
        "risk_tier": "T2",
        "rule": ("finance-governance", "Finance Governance", "Data sensitivity, disclaimers, and human review requirements."),
        "prompt": None,
    },
    "human-resources": {
        "name": "Human Resources",
        "description": "Job descriptions, interview kits, scorecards, and onboarding plans for people operations.",
        "tags": ["hr", "people-ops", "hiring", "onboarding"],
        "skills": ["job-description-writer", "interview-kit-builder", "interview-scorecard", "onboarding-plan"],
        "agent": ("hr-business-partner", "HR Business Partner", "human-resources"),
        "rule": ("hr-standards", "HR Standards", "Inclusive language, bias reduction, and PII handling."),
        "prompt": ("kickoff-hiring", "Kickoff Hiring Process", "Structure role definition and interview plan."),
    },
    "operations": {
        "name": "Operations",
        "description": "SOPs, process optimization, business cases, and status reporting for operational excellence.",
        "tags": ["operations", "sop", "process", "business-case"],
        "skills": ["sop-builder", "process-optimization", "business-case", "status-report"],
        "agent": ("operations-manager", "Operations Manager", "operations"),
        "rule": ("operations-standards", "Operations Standards", "Lean principles, measurable outcomes, and RACI clarity."),
        "prompt": None,
    },
    "program-management": {
        "name": "Program Management",
        "description": "RAID logs, stakeholder analysis, and program status reporting for multi-project delivery.",
        "tags": ["program-management", "raid", "stakeholders", "status"],
        "skills": ["raid-log", "stakeholder-analysis", "program-status-report"],
        "agent": None,
        "rule": ("program-management-standards", "Program Management Standards", "Governance, escalation paths, and dependency tracking."),
        "prompt": ("kickoff-program", "Kickoff Program Review", "Establish program context and reporting cadence."),
    },
    "legal-compliance": {
        "name": "Legal & Compliance",
        "description": "Contract review checklists and NDA triage — operational support, not legal advice.",
        "tags": ["legal", "compliance", "contracts", "nda"],
        "skills": ["contract-review-checklist", "nda-triage"],
        "agent": ("legal-ops-analyst", "Legal Ops Analyst", "legal-compliance"),
        "risk_tier": "T3",
        "rule": ("legal-disclaimer-standards", "Legal Disclaimer Standards", "Mandatory disclaimers and escalation to counsel."),
        "prompt": None,
    },
    "strategy-executive": {
        "name": "Strategy & Executive",
        "description": "Strategic planning, SWOT analysis, and competitive landscape for leadership decisions.",
        "tags": ["strategy", "executive", "swot", "competitive"],
        "skills": ["strategic-planning", "swot-analysis", "competitive-landscape"],
        "agent": None,
        "rule": ("executive-communication-standards", "Executive Communication Standards", "Concise, evidence-based leadership artifacts."),
        "prompt": ("kickoff-strategy", "Kickoff Strategy Session", "Frame strategic question and analysis approach."),
    },
    "communications": {
        "name": "Communications",
        "description": "Internal communications for org-wide announcements and change messaging.",
        "tags": ["communications", "internal-comms"],
        "skills": ["internal-comms"],
        "agent": None,
        "rule": ("comms-standards", "Communications Standards", "Tone, audience segmentation, and approval workflow."),
        "prompt": None,
    },
    "procurement-supply-chain": {
        "name": "Procurement & Supply Chain",
        "description": "RFP drafting and vendor evaluation for sourcing and supplier management.",
        "tags": ["procurement", "supply-chain", "rfp", "vendor"],
        "skills": ["rfp-draft", "vendor-evaluation"],
        "agent": None,
        "rule": ("procurement-standards", "Procurement Standards", "Fair evaluation, conflict of interest, and total cost of ownership."),
        "prompt": None,
    },
}

# Skill content: (name, description, when_to_use[], steps[(title, bullets[])], output, risk_tier?, disclaimer?)
SKILLS: dict = {}

def _load_skill_data() -> None:
    for part in ("_bundle_skills_data_part1.py", "_bundle_skills_data_part2.py",
                 "_bundle_skills_data_part3.py"):
        path = REPO / "scripts" / part
        if path.exists():
            exec(path.read_text(encoding="utf-8"), {"SKILLS": SKILLS})

# Inline document-processing skills
_SKILLS_DOC = {
    "docx-authoring": (
        "DOCX Authoring",
        "Create and edit Word documents with consistent structure, styles, and tracked changes. Use when producing reports, memos, or contracts from markdown or scratch.",
        [
            "Stakeholder needs a formal Word deliverable",
            "Converting research or markdown to client-ready DOCX",
            "Updating an existing document with version-controlled edits",
        ],
        [
            ("Gather requirements", [
                "Confirm audience, purpose, and template (if any)",
                "List required sections, appendices, and branding rules",
                "Identify whether tracked changes or comments are needed",
            ]),
            ("Structure the document", [
                "Apply heading hierarchy (H1–H3) using named styles, not manual bold",
                "Insert table of contents if document exceeds ~5 pages",
                "Use tables for structured data; avoid layout tables for positioning",
            ]),
            ("Author content", [
                "Write clear section intros and actionable conclusions",
                "Cross-reference figures and tables by number",
                "Keep paragraphs ≤ 5 sentences for executive readability",
            ]),
            ("Quality check", [
                "Verify style consistency and page breaks",
                "Run accessibility check: alt text, heading order, contrast",
                "Export PDF preview and compare against source requirements",
            ]),
        ],
        "Save as `doc/deliverables/<topic>.docx` with change log in companion markdown if needed.",
    ),
    "xlsx-analysis": (
        "XLSX Analysis",
        "Build and analyze Excel spreadsheets with formulas, pivot tables, and charts. Use for financial models, operational dashboards, and data summaries.",
        [
            "Analyzing tabular data with formulas or pivots",
            "Building a reusable spreadsheet template for a team",
            "Validating imported CSV data before downstream use",
        ],
        [
            ("Define the model", [
                "Separate inputs (assumptions), calculations, and outputs on distinct sheets",
                "Document units and source of each assumption cell",
                "Use named ranges for key inputs referenced across sheets",
            ]),
            ("Build calculations", [
                "Prefer structured references (Excel tables) over loose ranges",
                "Avoid hard-coded constants in formulas — reference assumption cells",
                "Add data validation for dropdown inputs where applicable",
            ]),
            ("Visualize and summarize", [
                "Choose chart types that match the message (trend vs composition)",
                "Add pivot tables for slice-and-dice exploration",
                "Include a summary dashboard sheet with KPI callouts",
            ]),
            ("Validate", [
                "Spot-check formulas with edge cases (zero, negative, null)",
                "Compare totals against source system exports",
                "Lock formula cells and protect structure before sharing",
            ]),
        ],
        "Deliver `doc/analysis/<topic>.xlsx` plus a one-page interpretation in markdown.",
    ),
    "pptx-generation": (
        "PPTX Generation",
        "Create slide decks with narrative flow, visual hierarchy, and speaker notes. Use for executive briefings, pitch decks, and workshop materials.",
        [
            "Turning a report or analysis into a presentation",
            "Building a template-compliant deck for leadership review",
            "Workshop or training slide materials",
        ],
        [
            ("Define narrative arc", [
                "One-sentence takeaway for the entire deck",
                "Outline: context → insight → recommendation → next steps",
                "Target slide count (rule of thumb: 1 idea per slide)",
            ]),
            ("Design slides", [
                "Use master layouts; avoid text-heavy bullets (>6 lines)",
                "One chart or visual per slide when presenting data",
                "Consistent typography and color from brand guidelines",
            ]),
            ("Add speaker notes", [
                "Notes explain what to say, not duplicate slide text",
                "Include anticipated questions and backup slides if needed",
                "Mark slides as appendix vs main flow",
            ]),
            ("Review", [
                "Read deck in slide-sorter view for flow gaps",
                "Time rehearsal: ~1–2 minutes per main-flow slide",
                "Export PDF handout version if required",
            ]),
        ],
        "Save as `doc/presentations/<topic>.pptx` with optional PDF export.",
    ),
    "pdf-extraction": (
        "PDF Extraction",
        "Extract text, tables, and metadata from PDFs and merge or split documents. Use when ingesting contracts, invoices, or research papers.",
        [
            "Pulling tables or text from scanned or digital PDFs",
            "Merging multiple PDFs into a single deliverable",
            "Preparing PDF content for search or summarization",
        ],
        [
            ("Assess PDF type", [
                "Determine if text is selectable (digital) or requires OCR",
                "Note page count, encryption, and form fields",
                "Identify tables vs free text vs images",
            ]),
            ("Extract content", [
                "Extract text preserving heading structure where possible",
                "For tables, export to CSV/XLSX and validate row/column counts",
                "Capture metadata: title, author, creation date",
            ]),
            ("Clean and structure", [
                "Remove headers/footers and page numbers from body text",
                "Fix hyphenation and line-break artifacts from OCR",
                "Tag sections for downstream search or RAG chunking",
            ]),
            ("Merge or split (if needed)", [
                "Define page ranges for split outputs",
                "Add bookmarks for merged documents",
                "Verify file size and accessibility of output PDFs",
            ]),
        ],
        "Save extracted content under `doc/extracts/<source>-extract.md` and tables as CSV.",
    ),
}
SKILLS.update(_SKILLS_DOC)
_load_skill_data()

AGENT_SKILLS_MAP = {
    "product-manager": ["prd-writer", "feature-spec", "roadmap-builder", "feature-prioritization", "product-discovery"],
    "devops-engineer": ["ci-cd-pipeline", "deployment-strategy", "incident-response-runbook", "slo-sli-tracking"],
    "ml-engineer": ["prompt-engineering", "rag-pipeline-design", "prompt-evaluation", "llm-risk-review"],
    "data-analyst": ["sql-query-review", "data-exploration", "statistical-analysis", "dashboard-design", "kpi-definition"],
    "marketing-manager": ["campaign-plan", "content-marketing", "seo-audit", "landing-page-copy"],
    "account-executive": ["discovery-call-prep", "account-research", "draft-outreach", "competitive-battlecard"],
    "customer-success-manager": ["ticket-triage", "qbr-prep", "churn-analysis", "support-response-draft"],
    "fp-and-a-analyst": ["budget-plan", "financial-forecast", "variance-analysis", "unit-economics"],
    "hr-business-partner": ["job-description-writer", "interview-kit-builder", "onboarding-plan"],
    "legal-ops-analyst": ["contract-review-checklist", "nda-triage"],
    "operations-manager": ["sop-builder", "process-optimization", "business-case", "status-report"],
}

RULE_BODIES = {
    "document-standards": """# Document Standards

Apply when creating or editing office documents for any department.

## Formatting

- Use named styles for headings; never rely on manual font size changes
- One primary font family per document; limit accent colors to brand palette
- Tables must include header rows and alt text where exported to PDF

## Version control

- Filename pattern: `<topic>-v<major>.<minor>.<ext>`
- Record change summary in document properties or companion changelog
- Preserve tracked changes until final approval

## Accessibility

- Minimum 12pt body text for print; 4.5:1 contrast for text
- Describe charts in adjacent text or alt text
- Logical reading order for screen readers

## Handoff

- Link source data (XLSX, CSV) when deck or doc cites numbers
- Archive finals under `doc/deliverables/`""",
    "product-methodology": """# Product Methodology Standards

Outcome-driven product development for all PM artifacts.

## Problem first

- Every PRD opens with validated problem statement and target user
- Separate problem, solution, and success metrics explicitly
- Link discovery evidence (interviews, data) to requirements

## Prioritization

- Document framework used (RICE, MoSCoW, Kano) with scores
- Call out trade-offs and deferred scope
- Align roadmap items to measurable outcomes, not feature lists

## Delivery alignment

- Hand off to engineering via **feature-spec** or global **write-user-stories**
- Define acceptance criteria testable by QA
- Include rollout, analytics, and support implications

## Communication

- Executive summary ≤ 200 words on all stakeholder documents
- Use diagrams for user flows; tables for prioritization matrices""",
    "sre-standards": """# SRE Standards

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
- Rotate credentials per **secrets-management** skill after incidents""",
    "engineering-standards": """# General Engineering Standards

Language-agnostic software engineering practices.

## Code review

- Reviews are blocking for correctness, security, and maintainability
- Author provides context: intent, test plan, rollout notes
- Prefer small PRs (<400 lines changed) for effective review

## Design before build

- Use **system-design** or **technical-rfc** for cross-team or irreversible decisions
- Document trade-offs and rejected alternatives
- Link ADRs/RFCs from code comments where relevant

## Testing

- Tests prove behavior, not implementation details
- Follow test pyramid: many unit, fewer integration, minimal E2E
- No merge without CI green and reviewer approval

## Documentation

- Update changelogs and README for user-visible changes
- Deprecate with migration path, not silent removal""",
    "ai-governance-standards": """# AI Governance Standards

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
- Document chunking strategy and retrieval boundaries""",
    "data-quality-standards": """# Data Quality Standards

Reproducible analytics and trustworthy metrics.

## Definitions

- Every KPI has owner, formula, grain, and refresh cadence
- Document filters, exclusions, and known limitations
- Version metric definitions when logic changes

## Analysis hygiene

- Show SQL or notebook steps for reproducibility
- State confidence intervals or sample size for statistics
- Label exploratory findings vs confirmed conclusions

## Visualization

- Chart titles state the insight, not just the metric name
- Avoid dual axes that distort comparisons
- Use colorblind-safe palettes

## Handoff

- Archive datasets and queries with analysis outputs
- Link dashboard specs to underlying tables""",
    "security-review-standards": """# Security Review Standards

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
- Escalate suspected active compromise immediately""",
    "marketing-standards": """# Marketing Standards

Brand-aligned, measurable, and compliant marketing work.

## Goals

- Every campaign defines objective, audience, channel, budget, and KPIs
- Tie activities to funnel stage (awareness, consideration, conversion)
- Set measurement window before launch

## Compliance

- Email: CAN-SPAM/GDPR opt-in and unsubscribe requirements
- Claims must be substantiated; avoid superlatives without proof
- Disclose sponsored content per platform rules

## Brand

- Follow voice and visual guidelines
- Localize for market when running multi-region campaigns
- Legal review for regulated industries (finance, health)""",
    "sales-methodology": """# Sales Methodology Standards

Discovery-first selling aligned to CRM hygiene.

## Discovery

- Lead with questions; confirm pain, impact, and decision process
- Document MEDDPICC or BANT fields in CRM after every call
- No demo until success criteria are understood

## Outreach

- Personalize first line; avoid generic bulk templates
- One clear CTA per message
- Respect opt-out and frequency caps

## Competitive

- Battlecards cite verified differentiators, not FUD
- Update win/loss notes within 24 hours of decision
- Escalate discount exceptions per approval matrix""",
    "customer-success-standards": """# Customer Success Standards

Retention-focused customer engagement.

## Response quality

- Acknowledge emotion before solution in support replies
- Set explicit next-step and timeline on every customer touch
- Escalate SEV issues per SLA within defined windows

## Health

- Track product adoption, support volume, and sentiment signals
- Proactive outreach when health score drops below threshold
- QBRs tie value delivered to customer business outcomes

## Knowledge base

- Articles follow: problem → steps → verification → related links
- Update KB within 48 hours of recurring ticket themes""",
    "finance-governance": """# Finance Governance Standards

**Not financial advice.** All outputs require qualified finance review before decisions.

## Data sensitivity

- Do not include employee compensation or unreleased financials in prompts
- Use aggregated or anonymized data in examples
- Mark all forecasts as illustrative scenarios

## Disclaimers

- Include "Not financial advice" on every forecast and unit economics output
- State assumptions explicitly; run sensitivity on key drivers
- Flag material changes requiring CFO approval

## Controls

- Separate planning versions (draft vs approved)
- Audit trail for assumption changes
- Escalate tax, investment, and valuation questions to specialists""",
    "hr-standards": """# HR Standards

Inclusive hiring and people operations with PII protection.

## Inclusive language

- Job descriptions use gender-neutral titles and essential requirements only
- Avoid age-coded terms ("rockstar", "digital native")
- Include EEO statement where applicable

## Interview integrity

- Structured questions and scorecards for every role
- No protected-class questions (age, family, religion, health)
- Panel debrief uses rubric scores, not gut feel alone

## Privacy

- Redact candidate PII in shared documents
- Store interview notes in approved HR systems only
- Onboarding plans exclude compensation details unless authorized""",
    "operations-standards": """# Operations Standards

Lean, measurable operational deliverables.

## SOPs

- One process owner per SOP; review annually
- Format: purpose, scope, RACI, steps, exceptions, references
- Include measurable SLA or quality checkpoint per major step

## Business cases

- State problem, options, recommendation, and ROI/NPV assumptions
- Identify one-time vs recurring costs
- Define success metrics at 30/90/180 days

## Reporting

- Status reports use RAG with evidence, not opinion
- Escalate blockers with proposed resolution options""",
    "program-management-standards": """# Program Management Standards

Multi-project governance and stakeholder alignment.

## RAID

- Review RAID log weekly; assign owners to all new items
- Distinguish risks (future) from issues (present)
- Link dependencies to milestone dates in plan

## Stakeholders

- Map power/interest grid; define engagement frequency
- Tailor comms format to audience (exec vs team)
- Document decisions and dissent in steerco minutes

## Status

- Program reports cover scope, schedule, cost, benefits, risks
- Highlight decisions needed from leadership
- Track benefits realization, not just deliverable completion""",
    "legal-disclaimer-standards": """# Legal Disclaimer Standards

**Not legal advice.** Agent outputs support operational triage only.

## Mandatory disclaimer

Every legal-compliance skill output must include:

> This checklist is for operational triage only and does not constitute legal advice. Consult qualified counsel for binding decisions.

## Escalation

- Non-standard clauses → escalate to legal counsel
- Jurisdiction-specific terms → tag region and route to local counsel
- Never recommend signing, rejecting, or negotiating without human lawyer review

## Documentation

- Log contract type, counterparty, and checklist completion date
- Do not store privileged attorney-client communications in general repos""",
    "executive-communication-standards": """# Executive Communication Standards

Concise, evidence-based artifacts for leadership.

## Structure

- BLUF (bottom line up front) in first paragraph
- Recommendations before supporting detail
- Appendices for data tables and methodology

## Evidence

- Cite sources and dates for market or competitive claims
- Quantify impact where possible; label estimates
- Present options with pros/cons before single recommendation

## Length

- Executive briefings: 1 page or 5 slides main flow
- Strategic plans: 10–15 pages max excluding appendices""",
    "comms-standards": """# Communications Standards

Clear internal messaging across the organization.

## Audience

- Segment by role, region, and impact level
- Lead with what changes for the reader
- Include effective date, owner, and FAQ link

## Tone

- Direct, respectful, jargon-free
- Acknowledge uncertainty when plans are evolving
- Avoid surprise announcements without manager preview

## Approval

- Exec announcements require comms + leadership sign-off
- Crisis comms follow pre-approved holding statement templates""",
    "procurement-standards": """# Procurement Standards

Fair, transparent sourcing and vendor evaluation.

## RFP process

- Define requirements before inviting vendors
- Use weighted scoring matrix published to evaluators
- Document conflicts of interest declarations

## Evaluation

- Score against criteria, not vendor relationships
- Include total cost of ownership, not just license price
- Reference **vendor-evaluation** and **technology-scouting** for technical depth

## Records

- Retain RFP, responses, and scoring worksheets per retention policy
- Route contract signature through legal and procurement""",
}


def title_case_skill(skill_id: str) -> str:
    return " ".join(w.capitalize() for w in skill_id.replace("-", " ").split())


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def yaml_str(s: str) -> str:
    if "\n" in s or ":" in s:
        return ">- \n  " + s.replace("\n", "\n  ")
    return s


def skill_md(skill_id: str, bundle_tag: str) -> str:
    data = SKILLS[skill_id]
    name, desc, when, steps, output = data[:5]
    risk = data[5] if len(data) > 5 else None
    disclaimer = data[6] if len(data) > 6 else None
    tags = [bundle_tag.replace("_", "-"), skill_id.split("-")[0]]
    if risk:
        tags.append(f"risk-{risk.lower()}")

    lines = [
        "---",
        f"name: {skill_id}",
        f"description: >-",
        f"  {desc}",
        f"tags: [{', '.join(tags)}]",
        "---",
        "",
        f"# {name}",
        "",
    ]
    if disclaimer:
        lines.extend(["> **Disclaimer:** " + disclaimer, ""])
    lines.extend(["## When to Use", ""])
    for w in when:
        lines.append(f"- {w}")
    lines.extend(["", "## Procedure", ""])
    for i, (step_title, bullets) in enumerate(steps, 1):
        lines.append(f"### Step {i}: {step_title}")
        lines.append("")
        for b in bullets:
            lines.append(f"- {b}")
        lines.append("")
    lines.extend(["## Output", "", output, ""])
    if disclaimer:
        lines.extend([
            "## Governance",
            "",
            f"- Risk tier: **{risk}**" if risk else "",
            "- Requires human review before external use or binding decisions.",
            "- " + disclaimer,
            "",
        ])
    return "\n".join(line for line in lines if line is not None)


def skill_manifest(skill_id: str, bundle_tag: str) -> str:
    data = SKILLS[skill_id]
    name, desc = data[0], data[1]
    risk = data[5] if len(data) > 5 else None
    tag_list = f"[{bundle_tag}, {skill_id}]"
    extra = f"riskTier: {risk}\n" if risk else ""
    return f"""id: {skill_id}
type: skill
version: 1.0.0
name: {name}
description: >-
  {desc}
tags: {tag_list}
{extra}status: active
"""


def agent_md(agent_id: str, display: str, bundle_id: str, bundle_tag: str) -> str:
    skills = AGENT_SKILLS_MAP.get(agent_id, [])
    skill_lines = "\n".join(f"- **{s}**" for s in skills)
    rule_id = BUNDLES[bundle_id]["rule"][0]
    return f"""---
name: {display}
description: >-
  Role agent for {bundle_tag.replace('-', ' ')}: primary specialist applying department
  skills, rules, and Plan-First gate before deliverables.
tools: [read, edit, search, web, agent, todo]
---

# {display} Role Agent

You are the **{display}** — the primary specialist for the **{bundle_id}** bundle.

## Mandatory MCP skills

Before starting, call `list_skills` and load matching skills:
{skill_lines}

Follow **{rule_id}** rule for all outputs.

## Scope

**Owns:** Department deliverables aligned to bundle skills and stakeholder requests.

**Does not own:** Cross-department work outside bundle scope unless explicitly escalated. Hand off via appropriate skills or global agents.

## Plan-First gate

1. Classify request and confirm success criteria with user
2. Select appropriate skill(s) from bundle
3. Execute workflow with rule compliance
4. Deliver artifact in standard location
5. Recommend next steps and owners

## Outputs

- Artifacts under `doc/` paths defined by each skill
- Structured recommendations with assumptions stated
"""


def rule_md(rule_id: str) -> str:
    return RULE_BODIES[rule_id]


def prompt_md(prompt_id: str, name: str, bundle_tag: str) -> str:
    return f"""---
name: {name}
description: >-
  Structured kickoff for {bundle_tag.replace('-', ' ')} work: classify request,
  select skills and agents, and produce an initial plan.
tags: [{bundle_tag}, kickoff]
---

You are kicking off a **{bundle_tag.replace('-', ' ')}** thread.

## User input

> {{{{input}}}}

## Your tasks

1. Call `list_skills` and identify matching workflows for this bundle
2. Call `list_agents` and select the best role agent if available
3. Classify the request in one sentence
4. Define scope, success criteria, and expected deliverable
5. Propose a step-by-step plan with skill references
6. Ask the user to confirm before executing

Do not start deep work until the plan is approved.
"""


def bundle_manifest(bundle_id: str, cfg: dict) -> str:
    risk = cfg.get("risk_tier")
    risk_line = f"riskTier: {risk}\n" if risk else ""
    tags_yaml = "\n".join(f"  - {t}" for t in cfg["tags"])
    return f"""id: {bundle_id}
type: bundle
version: 1.0.0
name: {cfg['name']}
description: >-
  {cfg['description']}
maintainers:
  - name: Agent Hub
    id: agenthub
tags:
{tags_yaml}
{risk_line}status: active
skill_count: {len(cfg['skills'])}
"""


def generate_global_skill_authoring() -> None:
    base = REPO / "global" / "skills" / "skill-authoring"
    content = """---
name: skill-authoring
description: >-
  Author new Agent Hub skills with correct structure, frontmatter, manifests, and
  quality gates. Use when creating or upgrading bundle skills at scale.
tags: [meta, authoring, skill]
---

# Skill Authoring

Create production-quality Agent Hub skills that agents can discover and follow reliably.

## When to Use

- Adding a new skill to a bundle or global catalog
- Upgrading a stub skill to full workflow content
- Reviewing skill quality before merge

## Procedure

### Step 1: Define the skill contract

- Choose kebab-case `skill-id` matching directory name
- Write one-line `description` with **when-to-use trigger** (starts with "Use when...")
- Assign tags: department bundle tag + domain keywords
- Set `riskTier` in manifest if T2+ (finance, legal, HR sensitive)

### Step 2: Structure SKILL.md

Required sections:
1. YAML frontmatter (`name`, `description`, `tags`)
2. `# Title` matching human-readable name
3. `## When to Use` — 3–5 bullet triggers
4. `## Procedure` — numbered steps with actionable sub-bullets
5. `## Output` — file path pattern and format

Target **40–80 lines** of procedural content. Not a one-liner stub.

### Step 3: Create manifest.yaml

```yaml
id: <skill-id>
type: skill
version: 1.0.0
name: Human Name
description: >-
  Same as SKILL frontmatter description.
tags: [bundle-tag, domain]
riskTier: T1   # optional
status: active
```

### Step 4: Add references (optional)

- Put templates under `references/` for long forms
- Keep SKILL.md as the workflow; references as fill-in-the-blank

### Step 5: Quality review

- [ ] Description is discoverable via search keywords
- [ ] Procedure steps are ordered and testable
- [ ] Output path follows repo conventions (`doc/...`)
- [ ] Disclaimers present for regulated domains
- [ ] No secrets or customer PII in examples

### Step 6: Register in bundle

- Add skill directory under `bundles/<bundle>/skills/<skill-id>/`
- Update bundle `manifest.yaml` skill_count if used
- Validate with `Catalog().list_skills()` after install

## Output

New skill directory:
```
bundles/<bundle>/skills/<skill-id>/
  SKILL.md
  manifest.yaml
  references/   # optional
```

## Related

- Template starter: global `some-skill`
- Bundle architecture: `doc/research/agenthub-skills-expansion-catalog.md` §7
"""
    write(base / "SKILL.md", content)
    write(base / "manifest.yaml", """id: skill-authoring
type: skill
version: 1.0.0
name: Skill Authoring
description: >-
  Author new Agent Hub skills with correct structure, frontmatter, manifests, and
  quality gates. Use when creating or upgrading bundle skills at scale.
tags: [meta, authoring, skill]
status: active
""")


def main() -> None:
    stats = {"bundles": 0, "skills": 0, "agents": 0, "rules": 0, "prompts": 0}
    for bundle_id, cfg in BUNDLES.items():
        bundle_dir = REPO / "bundles" / bundle_id
        write(bundle_dir / "manifest.yaml", bundle_manifest(bundle_id, cfg))
        stats["bundles"] += 1

        bundle_tag = bundle_id
        for skill_id in cfg["skills"]:
            if skill_id not in SKILLS:
                raise KeyError(f"Missing skill definition: {skill_id}")
            skill_dir = bundle_dir / "skills" / skill_id
            write(skill_dir / "SKILL.md", skill_md(skill_id, bundle_tag))
            write(skill_dir / "manifest.yaml", skill_manifest(skill_id, bundle_tag))
            stats["skills"] += 1

        if cfg.get("agent"):
            agent_id, display, _ = cfg["agent"]
            agent_dir = bundle_dir / "agents" / agent_id
            write(agent_dir / f"{agent_id}.agent.md", agent_md(agent_id, display, bundle_id, bundle_tag))
            write(agent_dir / "manifest.yaml", f"""id: {agent_id}
type: agent
version: 1.0.0
name: {display}
description: >-
  Primary role agent for {cfg['name']} bundle with Plan-First gate.
tags: [{bundle_tag}, agent]
status: active
""")
            stats["agents"] += 1

        rule_id, rule_name, rule_desc = cfg["rule"]
        rule_dir = bundle_dir / "rules" / rule_id
        write(rule_dir / f"{rule_id}.instructions.md", rule_md(rule_id))
        write(rule_dir / "manifest.yaml", f"""id: {rule_id}
type: rule
version: 1.0.0
name: {rule_name}
description: >-
  {rule_desc}
tags: [{bundle_tag}, standards]
status: active
""")
        stats["rules"] += 1

        if cfg.get("prompt"):
            prompt_id, prompt_name, _ = cfg["prompt"]
            prompt_dir = bundle_dir / "prompts" / prompt_id
            write(prompt_dir / f"{prompt_id}.prompt.md", prompt_md(prompt_id, prompt_name, bundle_tag))
            write(prompt_dir / "manifest.yaml", f"""id: {prompt_id}
type: prompt
version: 1.0.0
name: {prompt_name}
description: >-
  Kickoff prompt for {cfg['name']} workflows.
tags: [{bundle_tag}, kickoff]
status: active
""")
            stats["prompts"] += 1

    generate_global_skill_authoring()
    stats["skills"] += 1
    print(f"Generated: {stats}")


if __name__ == "__main__":
    main()
