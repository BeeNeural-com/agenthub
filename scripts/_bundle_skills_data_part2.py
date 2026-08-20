# Part 2: SWE general, AI ops, data, security, marketing, sales
SKILLS.update({
    "code-review": (
        "Code Review",
        "Review pull requests for correctness, readability, security, and maintainability. Use for PR-level review distinct from full-repo structured audits.",
        [
            "Reviewing a teammate's pull request before merge",
            "Self-review checklist before requesting review",
            "Teaching standards through constructive PR feedback",
        ],
        [
            ("Understand change intent", [
                "Read PR description, linked ticket, and test plan",
                "Identify scope: bugfix, feature, refactor, chore",
                "Note files outside expected scope for discussion",
            ]),
            ("Evaluate correctness", [
                "Trace happy path and edge cases mentally or via tests",
                "Check error handling and resource cleanup",
                "Verify concurrency and transaction boundaries if applicable",
            ]),
            ("Assess quality", [
                "Naming clarity and function size",
                "Duplication vs appropriate abstraction",
                "Test coverage for changed behavior",
            ]),
            ("Security and performance", [
                "Input validation, authz, injection risks",
                "N+1 queries, unbounded loops, memory leaks",
                "Flag secrets or PII in logs",
            ]),
            ("Provide feedback", [
                "Separate blocking vs nit vs suggestion",
                "Explain why, not just what",
                "Approve when blocking issues resolved",
            ]),
        ],
        "PR comments in tracker; optional summary in review thread.",
    ),
    "test-driven-development": (
        "Test-Driven Development",
        "Apply red-green-refactor cycle when implementing behavior. Use for new logic where tests clarify requirements.",
        [
            "Implementing well-defined business logic",
            "Bug fix that needs regression test",
            "Refactoring with safety net",
        ],
        [
            ("Red — write failing test", [
                "One behavior assertion per test when possible",
                "Use descriptive test names (should_X_when_Y)",
                "Confirm test fails for right reason",
            ]),
            ("Green — minimal implementation", [
                "Write simplest code to pass",
                "Avoid speculative features",
                "Run full relevant test suite",
            ]),
            ("Refactor — improve design", [
                "Remove duplication while tests stay green",
                "Improve names and extract functions",
                "Do not change behavior during refactor",
            ]),
            ("Repeat", [
                "Take next smallest behavior slice",
                "Keep commits small: test + implementation pairs",
                "Document any untestable seams for follow-up",
            ]),
        ],
        "Tests in repo test directory; behavior documented in PR.",
    ),
    "testing-strategy": (
        "Testing Strategy",
        "Define test pyramid, coverage goals, and test types for a project or release. Use when test approach is ad hoc or quality gaps appear.",
        [
            "New project test setup",
            "Release quality gate definition",
            "High escape rate from production bugs",
        ],
        [
            ("Assess context", [
                "System type: API, UI, batch, embedded",
                "Risk areas: payments, auth, data integrity",
                "Current test inventory and CI runtime budget",
            ]),
            ("Design pyramid", [
                "Unit: fast, isolated, high count",
                "Integration: contracts between modules/services",
                "E2E: critical user journeys only",
            ]),
            ("Define policies", [
                "Coverage targets per layer (not single global %)",
                "Required tests for bug fixes and new features",
                "Flake quarantine and SLA to fix",
            ]),
            ("Tooling and CI", [
                "Select frameworks aligned to stack",
                "Parallelize CI; cache fixtures",
                "Report test metrics in release checklist",
            ]),
        ],
        "Save as `doc/engineering/testing-strategy.md`.",
    ),
    "system-design": (
        "System Design",
        "Design distributed systems with capacity, consistency, and failure modes. Use for new services or major scalability changes.",
        [
            "Design interview or architecture review prep",
            "Scaling service beyond current limits",
            "Splitting monolith or adding async processing",
        ],
        [
            ("Requirements", [
                "Functional requirements and SLAs (QPS, latency, durability)",
                "Consistency model needs (strong vs eventual)",
                "Regulatory or residency constraints",
            ]),
            ("High-level design", [
                "Draw components: clients, APIs, workers, stores, queues",
                "Define data flow for read and write paths",
                "Identify single points of failure",
            ]),
            ("Deep dive critical paths", [
                "Estimate capacity with back-of-envelope math",
                "Choose storage and indexing strategy",
                "Plan caching and CDN if applicable",
            ]),
            ("Reliability", [
                "Failure scenarios: node loss, partition, dependency down",
                "Mitigations: retry, circuit breaker, bulkhead",
                "Observability per **monitoring-setup**",
            ]),
        ],
        "Save as `doc/engineering/system-design-<topic>.md` with diagrams.",
    ),
    "software-architecture": (
        "Software Architecture",
        "Apply architecture principles, patterns, and trade-off analysis for maintainable systems. Use for structural decisions within a codebase.",
        [
            "Evaluating module boundaries in a growing codebase",
            "Introducing a new architectural pattern",
            "Architecture review before major refactor",
        ],
        [
            ("Context and constraints", [
                "Team size, skill mix, and delivery timeline",
                "Quality attributes: modifiability, performance, security",
                "Existing architecture style and migration cost",
            ]),
            ("Evaluate patterns", [
                "Layered, hexagonal, event-driven, microservices — fit to context",
                "Document pros/cons for this system",
                "Reference SOLID and coupling/cohesion analysis",
            ]),
            ("Decision record", [
                "Capture decision, status, consequences",
                "Link to **technical-rfc** for cross-team decisions",
                "Identify validation milestones",
            ]),
            ("Governance", [
                "Define architecture fitness functions or lint rules",
                "Schedule periodic architecture reviews",
                "Align with **system-design** for distributed aspects",
            ]),
        ],
        "ADR in `doc/engineering/adr-<number>-<title>.md`.",
    ),
    "api-design": (
        "API Design",
        "Design REST, GraphQL, or gRPC APIs with consistent conventions and versioning. Use when exposing new or revised service interfaces.",
        [
            "Public or partner API design",
            "Internal service contract definition",
            "API redesign for breaking change management",
        ],
        [
            ("Model resources", [
                "Noun-based resources and consistent pluralization",
                "Represent relationships via URLs or embedded refs",
                "Define idempotency for mutating operations",
            ]),
            ("Request and response", [
                "Standard error envelope with codes and details",
                "Pagination, filtering, sorting conventions",
                "Use appropriate HTTP status codes",
            ]),
            ("Versioning and compatibility", [
                "URL or header versioning strategy",
                "Deprecation timeline and sunset headers",
                "Backward-compatible field additions only",
            ]),
            ("Documentation and testing", [
                "OpenAPI/Proto spec as source of truth",
                "Contract tests for consumers",
                "Rate limits and auth documented",
            ]),
        ],
        "OpenAPI/Proto spec in repo; summary in `doc/engineering/api-<name>.md`.",
    ),
    "changelog-generator": (
        "Changelog Generator",
        "Produce user-facing release notes from commits, PRs, or tickets. Use before product or engineering releases.",
        [
            "Preparing release notes for customers or internal users",
            "Summarizing sprint deliverables for stakeholders",
            "Documenting breaking changes for upgrade guides",
        ],
        [
            ("Collect changes", [
                "Gather merged PRs since last release tag",
                "Group by type: feature, fix, breaking, internal",
                "Exclude noise: chores, dependency-only bumps unless security",
            ]),
            ("Write for audience", [
                "User-facing: outcome language, not commit hashes",
                "Developers: migration steps for breaking changes",
                "Link to docs and KB articles",
            ]),
            ("Highlight impact", [
                "Call out security fixes without exploit detail",
                "Note performance improvements with benchmarks if available",
                "Thank contributors if open source",
            ]),
            ("Publish", [
                "Follow Keep a Changelog or team format",
                "Sync version in package manifests",
                "Coordinate with support and marketing on major releases",
            ]),
        ],
        "Update `CHANGELOG.md` and optional `doc/releases/v<version>.md`.",
    ),
    "technical-rfc": (
        "Technical RFC",
        "Author request-for-comments documents for significant technical decisions. Use when change affects multiple teams or is hard to reverse.",
        [
            "Cross-team protocol or platform change",
            "Technology adoption with org-wide impact",
            "Controversial design needing consensus",
        ],
        [
            ("RFC header", [
                "Title, author, status (draft/proposed/accepted/deprecated)",
                "Reviewers and decision deadline",
            ]),
            ("Problem and goals", [
                "Context and motivation",
                "Goals and non-goals",
                "Success metrics post-implementation",
            ]),
            ("Proposal", [
                "Detailed design with diagrams",
                "Alternatives considered and rejected",
                "Migration and rollout plan",
            ]),
            ("Review process", [
                "Comment period and office hours",
                "Resolve objections or document dissent",
                "Final decision and ADR linkage",
            ]),
        ],
        "Save as `doc/engineering/rfc-<number>-<title>.md`.",
    ),
    "prompt-engineering": (
        "Prompt Engineering",
        "Design system prompts, few-shot examples, and tool instructions for reliable LLM behavior. Use when building or tuning AI features.",
        [
            "New LLM-powered feature or agent",
            "Existing prompts show inconsistency or drift",
            "Migrating to a different model family",
        ],
        [
            ("Define task contract", [
                "Input/output schema and edge cases",
                "Tone, length, and format constraints",
                "Tools the model may call and when",
            ]),
            ("Draft system prompt", [
                "Role, rules, and refusal boundaries",
                "Step-by-step reasoning instruction if needed",
                "Examples: 2–5 diverse few-shot pairs",
            ]),
            ("Harden", [
                "Add anti-injection and scope limits",
                "Specify citation or 'I don't know' behavior",
                "Remove conflicting instructions",
            ]),
            ("Iterate with eval", [
                "Run **prompt-evaluation** regression set",
                "Compare models on cost/latency/quality",
                "Version prompts in git with changelog",
            ]),
        ],
        "Prompt files in repo + eval results in `doc/ai/prompt-<feature>.md`.",
    ),
    "prompt-evaluation": (
        "Prompt Evaluation",
        "Build test sets and metrics to regression-test prompts and models. Use before promoting prompt changes to production.",
        [
            "Before deploying prompt or model change",
            "Investigating quality regression in production",
            "Comparing model candidates",
        ],
        [
            ("Define eval set", [
                "Cover happy path, edge cases, adversarial inputs",
                "Include real anonymized production samples",
                "Label expected outputs or rubric criteria",
            ]),
            ("Choose metrics", [
                "Exact match, LLM-judge, human rubric as appropriate",
                "Track latency, token cost, refusal rate",
                "Separate safety eval from task accuracy",
            ]),
            ("Run experiments", [
                "Baseline current production prompt",
                "A/B candidate prompts on same set",
                "Statistical note if sample size small",
            ]),
            ("Gate release", [
                "Define pass thresholds per metric",
                "Document failures and mitigations",
                "Schedule periodic re-eval as model updates",
            ]),
        ],
        "Save eval report as `doc/ai/eval-<feature>-<date>.md`.",
    ),
    "rag-pipeline-design": (
        "RAG Pipeline Design",
        "Design retrieval-augmented generation pipelines: ingestion, chunking, retrieval, reranking. Use for knowledge-base Q&A features.",
        [
            "Building internal doc search + Q&A",
            "Improving RAG accuracy or hallucination rate",
            "Adding new document sources to existing RAG",
        ],
        [
            ("Source inventory", [
                "List document types, update frequency, access control",
                "Define metadata fields for filtering",
                "Plan PII redaction before indexing",
            ]),
            ("Chunking strategy", [
                "Chunk size vs context window tradeoff",
                "Overlap for continuity; respect section boundaries",
                "Store chunk provenance for citations",
            ]),
            ("Retrieval stack", [
                "Embedding model and vector index choice",
                "Hybrid search: semantic + keyword if needed",
                "Reranker for top-k precision",
            ]),
            ("Generation guardrails", [
                "Require citations from retrieved chunks",
                "Fallback when retrieval confidence low",
                "Monitor via **llm-risk-review** checklist",
            ]),
        ],
        "Architecture doc at `doc/ai/rag-<product>.md`.",
    ),
    "llm-risk-review": (
        "LLM Risk Review",
        "Review LLM features for safety, bias, data leakage, and abuse scenarios. Use before launch or after incidents.",
        [
            "Pre-launch review of customer-facing LLM feature",
            "Red-team findings need remediation plan",
            "Policy update for AI governance tier",
        ],
        [
            ("Data risks", [
                "Training/fine-tune data provenance and consent",
                "Prompt/response logging and retention",
                "Cross-tenant leakage in RAG indexes",
            ]),
            ("Safety and abuse", [
                "Jailbreak and prompt injection test cases",
                "Harmful content categories and refusals",
                "Rate limits and anomaly detection",
            ]),
            ("Fairness and bias", [
                "Test across demographic slices where applicable",
                "Document known limitations in UX",
                "Human review path for high-stakes outputs",
            ]),
            ("Sign-off", [
                "Assign risk tier T0–T3",
                "List required mitigations before GA",
                "Schedule periodic re-review",
            ]),
        ],
        "Risk assessment at `doc/ai/risk-review-<feature>.md`.",
    ),
    "agent-workflow-design": (
        "Agent Workflow Design",
        "Design multi-step agent workflows with tools, gates, and human checkpoints. Use for autonomous task automation.",
        [
            "Building Cursor/Agent Hub style multi-tool workflow",
            "Replacing brittle script chain with agent orchestration",
            "Adding human-in-the-loop approval steps",
        ],
        [
            ("Decompose task", [
                "Break into steps with clear inputs/outputs",
                "Identify which steps need tools vs LLM reasoning",
                "Mark irreversible actions for human gate",
            ]),
            ("Tool design", [
                "Minimal tool set; clear descriptions for model",
                "Idempotent tools where possible",
                "Timeout and retry policy per tool",
            ]),
            ("State and memory", [
                "What persists between steps (scratchpad, files)",
                "Avoid unbounded context growth",
                "Log trajectories for debugging",
            ]),
            ("Validate", [
                "Run golden-path and failure scenarios",
                "Measure cost and latency per workflow run",
                "Document escalation to human operator",
            ]),
        ],
        "Workflow spec at `doc/ai/agent-workflow-<name>.md`.",
    ),
    "sql-query-review": (
        "SQL Query Review",
        "Review and improve SQL for correctness, performance, and safety. Use before running analytics or production queries.",
        [
            "Analyst-generated query before production run",
            "Slow query optimization request",
            "Preventing accidental full table scans or PII exposure",
        ],
        [
            ("Correctness", [
                "Verify joins preserve intended grain",
                "Check NULL handling and duplicate row risk",
                "Validate filters match business definition",
            ]),
            ("Performance", [
                "EXPLAIN plan review for large tables",
                "Push filters early; avoid SELECT *",
                "Consider materialized views or pre-aggregation",
            ]),
            ("Safety", [
                "Read-only role for analytics",
                "LIMIT on exploratory queries",
                "No PII columns unless authorized",
            ]),
            ("Documentation", [
                "Comment non-obvious business logic",
                "Save canonical query to repo or dbt",
                "Link to **kpi-definition** if metric query",
            ]),
        ],
        "Reviewed query in repo or `doc/analytics/queries/<name>.sql`.",
    ),
    "data-exploration": (
        "Data Exploration",
        "Exploratory data analysis workflow: profiling, distributions, anomalies. Use when understanding a new dataset.",
        [
            "New data source for analytics project",
            "Unexpected metric movement investigation",
            "Pre-modeling data understanding",
        ],
        [
            ("Understand schema", [
                "Column types, null rates, cardinality",
                "Primary keys and relationship guesses",
                "Sample rows and time range coverage",
            ]),
            ("Profile distributions", [
                "Histograms for numeric; value counts for categorical",
                "Detect outliers and impossible values",
                "Compare segments (region, product, cohort)",
            ]),
            ("Hypothesis sketch", [
                "Note patterns worth deeper **statistical-analysis**",
                "Document data quality issues for upstream fix",
                "Avoid concluding causation from correlation alone",
            ]),
            ("Share findings", [
                "Executive summary with 3 key charts",
                "Reproducible notebook or SQL scripts",
                "Recommend next analysis steps",
            ]),
        ],
        "Notebook or report at `doc/analytics/eda-<topic>.md`.",
    ),
    "statistical-analysis": (
        "Statistical Analysis",
        "Apply appropriate statistical tests and interpret results with uncertainty. Use for experiments and hypothesis testing.",
        [
            "A/B test or experiment readout",
            "Comparing groups with significance testing",
            "Forecast confidence intervals",
        ],
        [
            ("Frame hypothesis", [
                "Null and alternative hypotheses",
                "Primary metric and guardrail metrics",
                "Minimum detectable effect if power analysis needed",
            ]),
            ("Check assumptions", [
                "Sample size and randomization quality",
                "Normality or use non-parametric tests",
                "Multiple comparison correction if many tests",
            ]),
            ("Run analysis", [
                "Report effect size, not only p-value",
                "Include confidence intervals",
                "Segment analysis with multiplicity caution",
            ]),
            ("Interpret", [
                "Practical vs statistical significance",
                "Limitations and confounders",
                "Recommendation: ship, extend test, or stop",
            ]),
        ],
        "Report at `doc/analytics/analysis-<experiment>.md`.",
    ),
    "dashboard-design": (
        "Dashboard Design",
        "Spec KPI dashboards with layout, filters, and drill paths. Use when building BI dashboards for teams or executives.",
        [
            "New Looker/Tableau/Power BI dashboard request",
            "Redesign of unused or confusing dashboard",
            "Executive metrics review preparation",
        ],
        [
            ("Audience and decisions", [
                "Who views daily vs weekly; what decisions they make",
                "One primary question per dashboard",
                "Mobile vs desktop usage",
            ]),
            ("Metric selection", [
                "Use **kpi-definition** for each tile",
                "Leading vs lagging indicators balance",
                "Max 7±2 tiles above fold",
            ]),
            ("Layout and interaction", [
                "F-pattern: summary top-left",
                "Global filters: date, region, product",
                "Drill to detail with row-level security",
            ]),
            ("Validation", [
                "Reconcile totals to source reports",
                "User test with 2 representative viewers",
                "Document refresh schedule and owner",
            ]),
        ],
        "Spec at `doc/analytics/dashboard-<name>.md`.",
    ),
    "kpi-definition": (
        "KPI Definition",
        "Define metrics with formula, grain, owner, and targets. Use when teams disagree on numbers or building new scorecards.",
        [
            "New product or business KPI needed",
            "Metric mismatch between teams",
            "OKR or executive scorecard setup",
        ],
        [
            ("Name and purpose", [
                "Business question the KPI answers",
                "Single owner accountable for definition",
                "Category: growth, quality, efficiency, satisfaction",
            ]),
            ("Formula", [
                "Numerator, denominator, filters, inclusions/exclusions",
                "Grain: user, account, order, day",
                "SQL or pseudocode for implementation",
            ]),
            ("Targets and thresholds", [
                "Baseline historical value",
                "Target and alert thresholds",
                "Review cadence (weekly/monthly/quarterly)",
            ]),
            ("Governance", [
                "Version definition changes in changelog",
                "Link dashboard tiles to this doc",
                "Align with finance definitions where overlapping",
            ]),
        ],
        "Catalog entry at `doc/analytics/kpi/<metric-id>.md`.",
    ),
    "threat-modeling": (
        "Threat Modeling",
        "Systematic threat analysis using STRIDE or attack trees for features and systems. Use during design or security review.",
        [
            "New feature handling auth, payments, or sensitive data",
            "Architecture change with expanded attack surface",
            "Annual security review of critical service",
        ],
        [
            ("Diagram system", [
                "Data flow diagram with trust boundaries",
                "Entry points, assets, and external dependencies",
                "Identify STRIDE categories per component",
            ]),
            ("Identify threats", [
                "Spoofing, tampering, repudiation, info disclosure, DoS, elevation",
                "Prioritize by likelihood × impact",
                "Note existing controls",
            ]),
            ("Mitigations", [
                "Map threats to controls or new work items",
                "Accept residual risk with sign-off for low items",
                "Link to **owasp-top10-review** where applicable",
            ]),
            ("Track", [
                "Store model with version and review date",
                "Re-run on major design changes",
                "Feed findings to sprint backlog",
            ]),
        ],
        "Threat model at `doc/security/threat-model-<system>.md`.",
    ),
    "owasp-top10-review": (
        "OWASP Top 10 Review",
        "Review application against OWASP Top 10 web risks with remediation guidance. Use for web app security assessments.",
        [
            "Pre-release security checklist for web app",
            "Pen test prep or finding triage",
            "Annual app security hygiene review",
        ],
        [
            ("Scope application", [
                "List endpoints, auth model, data classification",
                "Identify frameworks and dependency versions",
                "Note API vs server-rendered vs SPA",
            ]),
            ("Assess each category", [
                "Broken access control, cryptographic failures, injection, etc.",
                "Evidence: code path, config, or test result",
                "Rate: pass, partial, fail",
            ]),
            ("Remediate", [
                "Critical/high findings block release",
                "Provide fix pattern, not only CWE ID",
                "Retest after fix",
            ]),
            ("Report", [
                "Summary for engineering manager",
                "Detailed findings for developers",
                "Track in vulnerability backlog",
            ]),
        ],
        "Report at `doc/security/owasp-review-<app>-<date>.md`.",
    ),
    "secrets-scanning": (
        "Secrets Scanning",
        "Scan repositories, CI logs, and artifacts for exposed secrets. Use in CI and after suspected leakage.",
        [
            "Setting up pre-commit or CI secret detection",
            "Investigating leaked credential alert",
            "Onboarding new repo to security baseline",
        ],
        [
            ("Configure scanners", [
                "Enable git history scan on repo add",
                "Custom patterns for org-specific tokens",
                "Integrate with CI blocking on findings",
            ]),
            ("Triage findings", [
                "Verify true positive vs test fixtures",
                "Assess exposure: committed, public, forked",
                "Rotate credentials if ever in git history",
            ]),
            ("Remediate", [
                "Remove secret from history if policy requires (BFG/filter-repo)",
                "Move to vault; inject via CI secrets",
                "Add allowlist only with justification",
            ]),
            ("Prevent recurrence", [
                "Developer training on env vars",
                "Pre-commit hooks locally",
                "Audit quarterly",
            ]),
        ],
        "Scan report at `doc/security/secrets-scan-<repo>-<date>.md`.",
    ),
    "vulnerability-triage": (
        "Vulnerability Triage",
        "Prioritize CVEs and security findings by exploitability and asset criticality. Use when scanner output overwhelms capacity.",
        [
            "Dependency scan produced hundreds of CVEs",
            "Pen test report needs remediation plan",
            "Zero-day affecting stack component",
        ],
        [
            ("Inventory findings", [
                "Source: SCA, container scan, pen test",
                "Dedupe by CVE + affected component",
                "Map to owning service team",
            ]),
            ("Score risk", [
                "CVSS adjusted for context: network exposure, auth required",
                "Known exploit in wild elevates priority",
                "Compensating controls documented",
            ]),
            ("Decide action", [
                "Patch, mitigate, accept, defer with expiry",
                "SLA by severity tier",
                "Escalate critical to incident if active exploit",
            ]),
            ("Track to closure", [
                "Ticket per finding with verification step",
                "Report metrics to security leadership",
                "Feed patterns into **threat-modeling** updates",
            ]),
        ],
        "Triage sheet at `doc/security/vuln-triage-<date>.md`.",
    ),
})
