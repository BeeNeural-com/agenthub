# Remaining P0 skill definitions — imported by generate_phase1_3_bundles.py
# Format: (name, description, when_to_use[], steps[(title, bullets[])], output, risk_tier?, disclaimer?)

SKILLS.update({
    "prd-writer": (
        "PRD Writer",
        "Write product requirements documents with problem context, goals, scope, and acceptance criteria. Use when defining a new feature or major enhancement for engineering handoff.",
        [
            "Starting a new feature from validated discovery",
            "Consolidating stakeholder input into a single source of truth",
            "Preparing handoff from product to engineering sprint",
        ],
        [
            ("Problem and goals", [
                "State user problem, target persona, and business outcome",
                "Define success metrics (primary + guardrails)",
                "List non-goals explicitly to prevent scope creep",
            ]),
            ("Solution overview", [
                "Describe user journey at high level (not UI mockups unless ready)",
                "Identify dependencies on other teams or systems",
                "Note technical constraints from engineering preview",
            ]),
            ("Requirements", [
                "Number functional requirements (FR-001…)",
                "Add acceptance criteria in Given/When/Then format",
                "Include edge cases, error states, and accessibility needs",
            ]),
            ("Rollout and analytics", [
                "Define launch phases (internal, beta, GA)",
                "List events and dashboards for success measurement",
                "Document support and documentation implications",
            ]),
        ],
        "Save as `doc/product/prd-<feature>.md` and link from roadmap item.",
    ),
    "feature-spec": (
        "Feature Spec",
        "Detailed feature specification with user flows, data model, and API touchpoints. Use when PRD is approved and engineering needs implementation detail.",
        [
            "Engineering kickoff for a scoped feature",
            "Breaking an epic into implementable specification",
            "Aligning design and engineering on behavior",
        ],
        [
            ("Context", [
                "Link parent PRD and related user stories",
                "Summarize scope boundary for this spec",
                "List open questions with owners",
            ]),
            ("User flows", [
                "Document happy path and primary alternates",
                "Include state diagrams for complex interactions",
                "Define empty, loading, and error states",
            ]),
            ("Technical design", [
                "Outline data model changes and migrations",
                "List API endpoints or events with payloads",
                "Note performance, security, and i18n requirements",
            ]),
            ("Test plan", [
                "Map acceptance criteria to test types (unit, integration, E2E)",
                "Identify feature flags and rollback plan",
                "Define demo script for sprint review",
            ]),
        ],
        "Save as `doc/product/spec-<feature>.md`.",
    ),
    "roadmap-builder": (
        "Roadmap Builder",
        "Build time-phased product roadmaps aligned to strategy and capacity. Use for quarterly planning or stakeholder roadmap reviews.",
        [
            "Quarterly or PI roadmap planning",
            "Communicating sequencing trade-offs to leadership",
            "Reconciling requests against team capacity",
        ],
        [
            ("Strategic alignment", [
                "Link roadmap themes to company OKRs or strategy pillars",
                "Group initiatives into now / next / later horizons",
                "Identify bet vs incremental vs maintenance work",
            ]),
            ("Initiative catalog", [
                "List initiatives with outcome, effort (T-shirt), and owner",
                "Tag dependencies between initiatives",
                "Mark customer commitments vs optional bets",
            ]),
            ("Capacity check", [
                "Map initiatives to available squads or streams",
                "Highlight overcommitment and deferral candidates",
                "Include buffer for incidents and tech debt",
            ]),
            ("Communication layer", [
                "Executive view: themes and outcomes only",
                "Team view: milestones and dependencies",
                "External view: sanitize confidential items",
            ]),
        ],
        "Save as `doc/product/roadmap-<period>.md` with optional slide export via **pptx-generation**.",
    ),
    "feature-prioritization": (
        "Feature Prioritization",
        "Prioritize features using RICE, MoSCoW, or Kano with documented scores. Use when backlog exceeds capacity or stakeholders disagree on order.",
        [
            "Backlog grooming with competing priorities",
            "PI or sprint planning input",
            "Responding to 'why isn't X first?' questions",
        ],
        [
            ("Select framework", [
                "RICE for growth features with estimable reach/impact",
                "MoSCoW for fixed-deadline releases",
                "Kano for delight vs table-stakes classification",
                "Document why this framework fits the context",
            ]),
            ("Score candidates", [
                "List 5–15 items max per session to avoid fatigue",
                "Use consistent scale definitions across scorers",
                "Capture assumptions behind each score",
            ]),
            ("Facilitate alignment", [
                "Compare scores; discuss outliers >2 points",
                "Separate must-ship commitments from ranked backlog",
                "Record dissent and revisit triggers",
            ]),
            ("Output ranked list", [
                "Publish ranked backlog with scores table",
                "Note deferred items and conditions to revisit",
                "Link top items to roadmap horizons",
            ]),
        ],
        "Save as `doc/product/prioritization-<date>.md`.",
    ),
    "user-research-synthesis": (
        "User Research Synthesis",
        "Synthesize interview and survey findings into themes, insights, and recommendations. Use after user research sessions or support trend analysis.",
        [
            "After 5+ user interviews on a topic",
            "Consolidating survey open-text responses",
            "Turning support tickets into product insights",
        ],
        [
            ("Prepare corpus", [
                "Collect notes, recordings metadata, and consent scope",
                "Anonymize participant identifiers",
                "Tag sessions by segment, scenario, and date",
            ]),
            ("Affinity mapping", [
                "Extract atomic observations (one idea per note)",
                "Cluster into themes without forcing single taxonomy",
                "Name themes with user-voice quotes as evidence",
            ]),
            ("Insight generation", [
                "Write insight statements: observation + implication",
                "Rate confidence (high/medium/low) by evidence volume",
                "Identify contradictions and segment differences",
            ]),
            ("Recommendations", [
                "Map top insights to opportunity areas",
                "Propose next research or discovery experiments",
                "Hand off validated problems to **product-discovery** or **prd-writer**",
            ]),
        ],
        "Save as `doc/product/research-synthesis-<topic>.md`.",
    ),
    "product-discovery": (
        "Product Discovery",
        "Structured discovery: problem validation, assumption mapping, and experiment design before building. Use at idea stage or when success metrics are unclear.",
        [
            "New product idea or major pivot",
            "Feature failed adoption — revisit problem fit",
            "Stakeholder solution request without validated user need",
        ],
        [
            ("Frame discovery question", [
                "Write hypothesis: We believe [user] has [problem] because [evidence gap]",
                "Define kill criteria — what would stop the initiative",
                "Set time box (typically 1–4 weeks)",
            ]),
            ("Assumption mapping", [
                "List desirability, viability, feasibility assumptions",
                "Rank by risk × uncertainty",
                "Pick top 3 assumptions to test first",
            ]),
            ("Run experiments", [
                "Choose method: interviews, prototype, fake door, concierge",
                "Define sample size and success threshold",
                "Document learnings without confirmation bias",
            ]),
            ("Decision", [
                "Proceed to PRD, pivot problem, or stop",
                "Update opportunity assessment with evidence links",
                "Communicate decision rationale to stakeholders",
            ]),
        ],
        "Save as `doc/product/discovery-<topic>.md`.",
    ),
    "sprint-planning": (
        "Sprint Planning",
        "Facilitate sprint planning with capacity, commitments, and sprint goal. Use at sprint start for agile teams.",
        [
            "Two-week (or team cadence) sprint kickoff",
            "Translating prioritized backlog into sprint backlog",
            "Aligning team on single sprint goal",
        ],
        [
            ("Prepare inputs", [
                "Review refined backlog items with acceptance criteria",
                "Confirm team capacity (PTO, on-call, holidays)",
                "Identify carryover from previous sprint",
            ]),
            ("Set sprint goal", [
                "One sentence outcome the sprint should achieve",
                "Ensure goal connects to product or PI objective",
                "Avoid goal that is only 'complete tickets'",
            ]),
            ("Commit backlog", [
                "Team pulls items they can finish per Definition of Done",
                "Split oversized stories; defer unclear items",
                "Identify dependencies and external blockers",
            ]),
            ("Close planning", [
                "Confirm owners for each story",
                "Note stretch goals separately from commitment",
                "Publish sprint backlog in tracker (Jira, etc.)",
            ]),
        ],
        "Output sprint goal and committed backlog in tracker; summary in `doc/product/sprint-<id>.md`.",
    ),
    "ci-cd-pipeline": (
        "CI/CD Pipeline",
        "Design and review CI/CD pipelines with build, test, security gates, and artifact promotion. Use when creating or improving delivery automation.",
        [
            "New service needs automated build and deploy",
            "Pipeline is slow, flaky, or bypassed by teams",
            "Adding security or compliance gates to delivery",
        ],
        [
            ("Map current flow", [
                "Document trigger events (PR, main merge, tag)",
                "List stages: lint, unit, integration, build, deploy",
                "Identify manual steps and mean time to feedback",
            ]),
            ("Design pipeline stages", [
                "Fail fast: cheapest checks first",
                "Parallelize independent jobs; cache dependencies",
                "Pin tool versions and use reproducible builds",
            ]),
            ("Add quality gates", [
                "Block merge on test coverage threshold if policy exists",
                "Run SAST/secret scan per **secrets-scanning**",
                "Require approval for production promotion",
            ]),
            ("Operationalize", [
                "Define artifact naming and retention",
                "Document rollback via **deployment-strategy**",
                "Monitor pipeline metrics (duration, flake rate)",
            ]),
        ],
        "Save pipeline spec as `doc/platform/ci-cd-<service>.md` and implement in CI config.",
    ),
    "deployment-strategy": (
        "Deployment Strategy",
        "Plan deployment approaches: rolling, blue/green, canary, and feature flags. Use before production releases or architecture changes.",
        [
            "Launching a high-risk or high-traffic change",
            "Designing zero-downtime deployment for a service",
            "Choosing rollback strategy before release day",
        ],
        [
            ("Assess change risk", [
                "Classify: config, code, schema, infrastructure",
                "Estimate blast radius and user impact",
                "Define success metrics for first hour/day",
            ]),
            ("Select strategy", [
                "Rolling: default for stateless services",
                "Blue/green: instant switch with double capacity cost",
                "Canary: progressive traffic shift with automated rollback",
                "Feature flags: decouple deploy from release",
            ]),
            ("Plan execution", [
                "Write step-by-step runbook with owners",
                "Define health checks and automatic abort criteria",
                "Schedule comms for customer-facing changes",
            ]),
            ("Validate rollback", [
                "Test rollback in staging or game day",
                "Document data migration rollback if applicable",
                "Set monitoring dashboards for release window",
            ]),
        ],
        "Save as `doc/platform/deployment-<release>.md`.",
    ),
    "incident-response-runbook": (
        "Incident Response Runbook",
        "Create and execute incident response runbooks for detection, mitigation, and communication. Use during active incidents or runbook authoring.",
        [
            "Active production incident (SEV1–SEV3)",
            "Authoring service-specific incident runbook",
            "On-call training and game day preparation",
        ],
        [
            ("Detect and declare", [
                "Confirm alert is not false positive",
                "Assign incident commander and severity",
                "Open incident channel and status page if SEV1/2",
            ]),
            ("Mitigate", [
                "Stop the bleeding: rollback, scale, disable feature",
                "Preserve evidence: logs, traces, recent deploys",
                "Time-box investigation spikes; prefer known fixes",
            ]),
            ("Communicate", [
                "Internal updates every 15–30 min for SEV1",
                "Customer comms via approved templates",
                "Document timeline in incident doc in real time",
            ]),
            ("Resolve and handoff", [
                "Confirm metrics restored and error budget impact",
                "Schedule postmortem per **incident-postmortem**",
                "Create follow-up tickets with owners",
            ]),
        ],
        "Active: incident doc in tracker. Runbook: `doc/runbooks/incident-<service>.md`.",
    ),
    "incident-postmortem": (
        "Incident Postmortem",
        "Facilitate blameless postmortems with timeline, root cause, and action items. Use within 5 business days of incident resolution.",
        [
            "After SEV1–SEV3 incident closure",
            "Recurring incident pattern needs systemic fix",
            "Game day or chaos exercise debrief",
        ],
        [
            ("Gather timeline", [
                "Collect UTC timestamps for detect, respond, mitigate, resolve",
                "Include deploy events, config changes, external deps",
                "Use scribe notes from incident channel",
            ]),
            ("Root cause analysis", [
                "Apply 5-whys or fault tree without blaming people",
                "Distinguish trigger vs contributing factors",
                "Note what went well in response",
            ]),
            ("Action items", [
                "Each item: owner, due date, priority, verification method",
                "Prefer preventive fixes over manual toil",
                "Track in same system as engineering backlog",
            ]),
            ("Publish and share", [
                "Review draft with incident participants",
                "Share summary org-wide for SEV1",
                "Link related runbook updates",
            ]),
        ],
        "Save as `doc/incidents/postmortem-<id>.md`.",
    ),
    "slo-sli-tracking": (
        "SLO/SLI Tracking",
        "Define SLIs, SLOs, error budgets, and alerting policies for services. Use when establishing or reviewing reliability targets.",
        [
            "New service going to production",
            "Error budget exhausted or alert fatigue review",
            "Quarterly reliability review with product",
        ],
        [
            ("Choose SLIs", [
                "Pick user-centric signals: availability, latency, correctness",
                "Define measurement window and aggregation (p99, success rate)",
                "Avoid monitoring only infrastructure metrics",
            ]),
            ("Set SLO targets", [
                "Align target with user expectations and contract SLAs",
                "Document rationale for chosen percentage",
                "Calculate error budget per period",
            ]),
            ("Alerting policy", [
                "Multi-window burn rate alerts for budget consumption",
                "Page only for SLO-threatening conditions",
                "Ticket for sub-SLO trends within budget",
            ]),
            ("Review cadence", [
                "Weekly error budget review with product owner",
                "Freeze features if budget exhausted (policy-dependent)",
                "Adjust SLOs with data, not optimism",
            ]),
        ],
        "Save as `doc/platform/slo-<service>.md` with dashboard links.",
    ),
    "monitoring-setup": (
        "Monitoring Setup",
        "Design metrics, logs, and traces with dashboards and alerts for a service. Use for new services or observability gaps.",
        [
            "Service lacks dashboards or actionable alerts",
            "On-call receives noise without clear remediation",
            "Migrating to OpenTelemetry or new observability stack",
        ],
        [
            ("Instrument", [
                "Add RED/USE metrics for each endpoint or queue",
                "Structured JSON logs with trace_id correlation",
                "Distributed tracing on critical paths",
            ]),
            ("Dashboard design", [
                "Golden signals overview dashboard per service",
                "Drill-down views for dependencies",
                "SLO dashboard linked to error budget",
            ]),
            ("Alert rules", [
                "Every alert links to runbook section",
                "Test alerts in staging before production",
                "Set severity: page vs ticket vs log-only",
            ]),
            ("Validate", [
                "Run failure injection to confirm alert fires",
                "Review cardinality and cost of high-cardinality labels",
                "Document ownership and on-call rotation",
            ]),
        ],
        "Save as `doc/platform/monitoring-<service>.md`.",
    ),
    "secrets-management": (
        "Secrets Management",
        "Manage secrets lifecycle: storage, rotation, scanning, and access control. Use when handling credentials, API keys, or certificates.",
        [
            "New service needs secrets injection pattern",
            "Credential rotation after incident or policy",
            "Remediating leaked secrets in repo or logs",
        ],
        [
            ("Inventory secrets", [
                "List secret types: API keys, DB passwords, certs, tokens",
                "Map consumers (services, humans, CI jobs)",
                "Classify sensitivity and rotation frequency",
            ]),
            ("Storage pattern", [
                "Use vault/KMS — never commit secrets to git",
                "Inject at runtime via env or sidecar",
                "Separate secrets per environment",
            ]),
            ("Rotation and access", [
                "Automate rotation where platform supports",
                "Apply least privilege and audit access logs",
                "Revoke compromised secrets immediately",
            ]),
            ("Prevent leakage", [
                "Enable pre-commit and CI secret scanning",
                "Scrub logs and error messages for secret patterns",
                "Run **secrets-scanning** after any exposure event",
            ]),
        ],
        "Save policy as `doc/platform/secrets-<scope>.md`; implement in vault/IaC.",
    ),
})
