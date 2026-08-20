# Part 3: marketing, sales, CS, finance, HR, ops, program, legal, strategy, comms, procurement
SKILLS.update({
    "campaign-plan": (
        "Campaign Plan",
        "End-to-end marketing campaign plan with objectives, audience, channels, timeline, and KPIs. Use when launching integrated campaigns.",
        [
            "Quarterly demand gen or product launch campaign",
            "Multi-channel campaign needing single plan",
            "Campaign retrospective input for next cycle",
        ],
        [
            ("Objective and audience", [
                "SMART goal tied to funnel stage",
                "ICP/persona and segment size estimate",
                "Offer and CTA definition",
            ]),
            ("Channel mix", [
                "Paid, owned, earned channels with budget split",
                "Message matrix by channel and persona",
                "Creative requirements and production timeline",
            ]),
            ("Execution timeline", [
                "Milestone calendar: build, launch, optimize, wrap",
                "Owners per workstream",
                "Dependencies on product, sales, legal",
            ]),
            ("Measurement", [
                "Primary KPI and secondary metrics",
                "UTM and attribution plan",
                "Mid-campaign optimization checkpoints",
            ]),
        ],
        "Save as `doc/marketing/campaign-<name>.md`.",
    ),
    "content-marketing": (
        "Content Marketing",
        "Plan and produce content marketing assets: blogs, whitepapers, case studies. Use for inbound and thought leadership.",
        [
            "Blog or whitepaper from product launch",
            "SEO-driven content cluster buildout",
            "Customer story or case study production",
        ],
        [
            ("Strategy alignment", [
                "Topic maps to persona pain and funnel stage",
                "Keyword research via **seo-content-optimization**",
                "Differentiation angle vs competitors",
            ]),
            ("Outline and draft", [
                "Hook, problem, insight, proof, CTA structure",
                "Include data, quotes, and visuals plan",
                "Expert review for technical accuracy",
            ]),
            ("Production", [
                "Editorial standards: tone, length, citations",
                "Accessibility: alt text, heading structure",
                "Legal/compliance review if regulated claims",
            ]),
            ("Distribution", [
                "Publish channels and promotion plan",
                "Repurpose into social, email, sales enablement",
                "Measure engagement and pipeline influence",
            ]),
        ],
        "Draft in `doc/marketing/content/<slug>.md`; publish to CMS.",
    ),
    "seo-audit": (
        "SEO Audit",
        "Technical and content SEO audit with prioritized fixes. Use for site health reviews or traffic decline investigation.",
        [
            "Organic traffic drop investigation",
            "Pre-launch site or migration review",
            "Quarterly SEO hygiene check",
        ],
        [
            ("Technical crawl", [
                "Indexability, robots, sitemap, canonicals",
                "Core Web Vitals and mobile usability",
                "Broken links, redirect chains, HTTPS",
            ]),
            ("On-page review", [
                "Title/meta, H1, internal linking",
                "Thin or duplicate content pages",
                "Schema markup opportunities",
            ]),
            ("Off-page snapshot", [
                "Backlink profile health (overview)",
                "Brand SERP and competitor comparison",
                "Local SEO if applicable",
            ]),
            ("Prioritize fixes", [
                "Impact × effort matrix",
                "Quick wins vs structural projects",
                "Hand content fixes to **seo-content-optimization**",
            ]),
        ],
        "Audit report at `doc/marketing/seo-audit-<date>.md`.",
    ),
    "seo-content-optimization": (
        "SEO Content Optimization",
        "Optimize pages for target keywords and search intent while maintaining readability. Use when updating or creating web content.",
        [
            "Blog or landing page needs ranking improvement",
            "New page targeting specific keyword cluster",
            "Refreshing declining content",
        ],
        [
            ("Keyword and intent", [
                "Primary and secondary keywords",
                "SERP analysis: format competitors use",
                "Match intent: informational vs transactional",
            ]),
            ("On-page optimization", [
                "Title tag ≤60 chars; meta ≤155 chars",
                "H1/H2 structure with natural keyword use",
                "Internal links to pillar and related pages",
            ]),
            ("Content quality", [
                "Cover subtopics users expect",
                "Add FAQ schema where appropriate",
                "Update publish date when materially refreshed",
            ]),
            ("Measure", [
                "Baseline rank and traffic before change",
                "Review at 4–8 weeks post-publish",
                "Iterate based on GSC queries",
            ]),
        ],
        "Optimization brief at `doc/marketing/seo/<page-slug>.md`.",
    ),
    "email-marketing": (
        "Email Marketing",
        "Design email sequences and campaigns with compliance and deliverability best practices. Use for nurture, launch, and lifecycle emails.",
        [
            "Drip nurture sequence for leads",
            "Product announcement email",
            "Re-engagement campaign for inactive users",
        ],
        [
            ("Audience and goal", [
                "Segment definition and list source consent",
                "Single CTA per email",
                "Success metric: open, click, conversion",
            ]),
            ("Copy and structure", [
                "Subject line A/B variants",
                "Scannable body: preview text, bullets, button",
                "Plain-text alternative for accessibility",
            ]),
            ("Compliance", [
                "CAN-SPAM: physical address, unsubscribe",
                "GDPR: lawful basis and preference center",
                "Avoid deceptive subject lines",
            ]),
            ("Deliverability", [
                "Authenticate SPF/DKIM/DMARC",
                "Warm new domains; monitor bounce/complaint rates",
                "Test across clients before send",
            ]),
        ],
        "Copy in `doc/marketing/email/<campaign>.md`; implement in ESP.",
    ),
    "landing-page-copy": (
        "Landing Page Copy",
        "Write conversion-focused landing page copy with clear value proposition and CTA. Use for campaigns and product pages.",
        [
            "Paid ads need dedicated landing page",
            "Product launch or feature landing page",
            "A/B test variant for headline or CTA",
        ],
        [
            ("Above the fold", [
                "Headline: outcome for target persona",
                "Subhead: how + differentiation",
                "Primary CTA verb-specific (Start trial, Book demo)",
            ]),
            ("Body sections", [
                "Social proof: logos, quotes, metrics",
                "Benefits before features; address objections",
                "FAQ for remaining friction",
            ]),
            ("Conversion elements", [
                "Form fields minimized for stage",
                "Trust badges and privacy reassurance",
                "Mobile-first scannability",
            ]),
            ("Test plan", [
                "Hypothesis for A/B variants",
                "Track micro-conversions",
                "Align message with ad **campaign-plan**",
            ]),
        ],
        "Copy doc at `doc/marketing/landing/<slug>.md`.",
    ),
    "discovery-call-prep": (
        "Discovery Call Prep",
        "Prepare discovery calls with hypothesis, questions, and success criteria. Use before first or expansion sales meetings.",
        [
            "First meeting with new prospect",
            "Qualification call after inbound lead",
            "Expansion conversation with existing customer",
        ],
        [
            ("Research account", [
                "Run **account-research** for context",
                "Identify stakeholders and likely pains",
                "Hypothesis on why they would buy now",
            ]),
            ("Question plan", [
                "Open-ended discovery questions (SPIN/MEDDPICC)",
                "Avoid premature demo pitch",
                "Confirm decision process and timeline",
            ]),
            ("Call structure", [
                "Agenda share in first 2 minutes",
                "Time boxes: discovery vs next steps",
                "Leave buffer for objections",
            ]),
            ("Success criteria", [
                "Minimum: pain, impact, next step scheduled",
                "Update CRM fields post-call",
                "Hand off gaps to **call-prep** for follow-up meeting",
            ]),
        ],
        "Brief at `doc/sales/discovery-<account>.md`.",
    ),
    "account-research": (
        "Account Research",
        "Build account intelligence: org structure, initiatives, tech stack, triggers. Use before outreach or QBR.",
        [
            "Target account planning for enterprise sale",
            "Pre-meeting intelligence gathering",
            "Territory planning prioritization",
        ],
        [
            ("Firmographics", [
                "Industry, size, geography, growth signals",
                "Recent news, funding, leadership changes",
                "Tech stack from job posts or integrations",
            ]),
            ("Stakeholder map", [
                "Economic buyer, champion, blockers",
                "LinkedIn roles and reporting hints",
                "Past vendor relationships if known",
            ]),
            ("Initiatives and pains", [
                "Public priorities: earnings, job listings, RFPs",
                "Hypothesized pains linked to your solution",
                "Competitive incumbents",
            ]),
            ("Actionable insights", [
                "3 talk tracks tailored to persona",
                "Trigger events for outreach timing",
                "Save to CRM account plan",
            ]),
        ],
        "Account plan at `doc/sales/accounts/<account>.md`.",
    ),
    "call-prep": (
        "Call Prep",
        "Prepare meeting briefs with agenda, talk tracks, and objection handling. Use before any significant sales meeting.",
        [
            "Demo or technical deep-dive meeting",
            "Executive sponsor meeting",
            "Negotiation or pricing discussion",
        ],
        [
            ("Meeting objective", [
                "Single desired outcome",
                "Attendee roles and what each cares about",
                "Link prior discovery notes",
            ]),
            ("Agenda draft", [
                "Share proactively with customer",
                "Time allocation per topic",
                "Questions to confirm understanding",
            ]),
            ("Talk tracks and assets", [
                "Relevant case studies and **competitive-battlecard**",
                "Demo storyline if applicable",
                "Pricing guardrails internal only",
            ]),
            ("Objections", [
                "Top 3 anticipated objections and responses",
                "Escalation path for non-standard asks",
                "Post-meeting CRM update checklist",
            ]),
        ],
        "Brief at `doc/sales/call-prep-<account>-<date>.md`.",
    ),
    "draft-outreach": (
        "Draft Outreach",
        "Write personalized sales outreach emails or LinkedIn messages. Use for prospecting sequences.",
        [
            "Cold outbound to target account",
            "Follow-up after event or content download",
            "Re-engage stalled opportunity",
        ],
        [
            ("Personalization", [
                "First line references specific account trigger",
                "Connect pain to relevant proof point",
                "Avoid fake familiarity",
            ]),
            ("Structure", [
                "≤120 words for cold email",
                "One ask: 15-min call or question reply",
                "P.S. optional second hook",
            ]),
            ("Sequence context", [
                "Email 1 value; email 2 proof; email 3 breakup",
                "Vary channel if no response",
                "Respect opt-out and frequency caps",
            ]),
            ("Compliance", [
                "CAN-SPAM/GDPR for email",
                "LinkedIn platform ToS",
                "No misleading subject lines",
            ]),
        ],
        "Templates at `doc/sales/outreach/<sequence>.md`.",
    ),
    "competitive-battlecard": (
        "Competitive Battlecard",
        "Create sales battlecards with positioning, strengths/weaknesses, and talk tracks vs competitors. Use for competitive deals.",
        [
            "Deal involves known competitor",
            "Sales enablement refresh quarterly",
            "New competitor entered market",
        ],
        [
            ("Competitor profile", [
                "Target market, pricing model, key features",
                "Recent product/news changes",
                "Win/loss themes from CRM",
            ]),
            ("Comparison", [
                "Feature matrix: us vs them (honest)",
                "Landmines: questions that expose their weaknesses",
                "Trap answers if they disparage us",
            ]),
            ("Talk tracks", [
                "Elevator differentiation",
                "Objection: 'We already use X'",
                "Proof points: customers who switched",
            ]),
            ("Maintenance", [
                "Owner and review date",
                "Source citations for claims",
                "Coordinate with marketing on messaging",
            ]),
        ],
        "Battlecard at `doc/sales/battlecards/<competitor>.md`.",
    ),
    "lead-qualification": (
        "Lead Qualification",
        "Qualify leads using BANT, MEDDIC, or team framework with documented rationale. Use for inbound routing and prioritization.",
        [
            "Inbound lead needs SDR qualification",
            "Marketing pass-off to sales",
            "Disqualify or nurture decision",
        ],
        [
            ("Framework selection", [
                "BANT for transactional; MEDDIC for enterprise",
                "Document required fields in CRM",
                "Scoring weights if automated",
            ]),
            ("Gather evidence", [
                "Discovery notes, form data, enrichment",
                "Identify missing fields to probe",
                "Note red flags: budget, fit, timing",
            ]),
            ("Decision", [
                "SQL → assign AE with handoff note",
                "Nurture → marketing sequence",
                "Disqualify → reason coded in CRM",
            ]),
            ("Feedback loop", [
                "Share disqualify reasons with marketing",
                "Calibrate scoring monthly",
                "Track conversion by source",
            ]),
        ],
        "Qualification record in CRM; summary in `doc/sales/qualification/<lead>.md`.",
    ),
    "ticket-triage": (
        "Ticket Triage",
        "Triage support tickets for priority, routing, and initial response SLA. Use in support queue management.",
        [
            "New ticket enters support queue",
            "Escalation from chat or social channel",
            "After-hours on-call support handoff",
        ],
        [
            ("Classify", [
                "Severity: outage vs question vs feature request",
                "Impact: users affected, revenue at risk",
                "Category: billing, technical, how-to",
            ]),
            ("Route", [
                "Assign team/skill based on category",
                "Link related incidents or known issues",
                "Merge duplicates",
            ]),
            ("SLA", [
                "First response within tier target",
                "Set customer expectation on resolution time",
                "Escalate SEV per runbook",
            ]),
            ("Document", [
                "Internal notes vs customer-visible reply",
                "Tag for KB gap if recurring theme",
                "Use **support-response-draft** for reply",
            ]),
        ],
        "Triage notes in ticket system.",
    ),
    "support-response-draft": (
        "Support Response Draft",
        "Draft empathetic, accurate customer support replies. Use when responding to tickets or social support.",
        [
            "Email or ticket response needed",
            "Sensitive customer frustration situation",
            "Technical issue requiring step-by-step guidance",
        ],
        [
            ("Acknowledge", [
                "Reflect customer issue in their words",
                "Apologize for impact without admitting liability if unclear",
                "Confirm understanding before solution",
            ]),
            ("Resolve or progress", [
                "Step-by-step instructions numbered",
                "Link KB articles via **kb-article-writer** output",
                "Set expectation if engineering fix needed",
            ]),
            ("Tone and clarity", [
                "Grade 8 reading level; avoid jargon",
                "One issue per reply when possible",
                "Sign with name and follow-up channel",
            ]),
            ("Close loop", [
                "Ask confirmation issue resolved",
                "Offer survey after resolution",
                "Flag product feedback themes",
            ]),
        ],
        "Reply in ticket system; save template variants in `doc/support/templates/`.",
    ),
    "kb-article-writer": (
        "KB Article Writer",
        "Write help center articles with problem-solution structure and search optimization. Use for self-service support content.",
        [
            "Recurring support theme needs documentation",
            "New feature launch enablement",
            "Refreshing outdated help article",
        ],
        [
            ("Define audience and problem", [
                "Who searches this and what words they use",
                "Symptoms vs root cause framing",
                "Prerequisites and permissions",
            ]),
            ("Structure article", [
                "Title: action-oriented",
                "Steps numbered with screenshots placeholders",
                "Verification: how user knows it worked",
            ]),
            ("Quality", [
                "Test steps on clean environment",
                "Link related articles",
                "Accessibility: alt text, headings",
            ]),
            ("Publish", [
                "SEO title and meta description",
                "Tag product area and version",
                "Review schedule every 6 months",
            ]),
        ],
        "Article draft at `doc/support/kb/<slug>.md`; publish to help center.",
    ),
    "qbr-prep": (
        "QBR Prep",
        "Prepare quarterly business review decks and narratives for customer accounts. Use before executive customer meetings.",
        [
            "Scheduled QBR with strategic account",
            "Renewal conversation needing value proof",
            "Executive sponsor alignment meeting",
        ],
        [
            ("Account context", [
                "Contract scope, goals, stakeholders",
                "Health signals: usage, support, NPS",
                "Open risks from **churn-analysis**",
            ]),
            ("Value narrative", [
                "Outcomes delivered vs success plan",
                "ROI metrics customer agreed matter",
                "Product roadmap relevant to them",
            ]),
            ("Deck structure", [
                "Executive summary, usage, wins, risks, next quarter plan",
                "Mutual action items with dates",
                "Ask: expansion, reference, feedback",
            ]),
            ("Rehearsal", [
                "Internal dry run with CSM + AE",
                "Anticipate hard questions",
                "Send pre-read 24h ahead if appropriate",
            ]),
        ],
        "Deck outline at `doc/customer-success/qbr/<account>-<quarter>.md`.",
    ),
    "churn-analysis": (
        "Churn Analysis",
        "Analyze churn patterns and build retention playbooks. Use when churn rises or at-risk accounts need intervention.",
        [
            "Monthly churn review",
            "Specific account cancellation post-mortem",
            "Designing retention campaign",
        ],
        [
            ("Quantify churn", [
                "Logo vs revenue churn by segment",
                "Cohort curves and tenure at churn",
                "Compare to historical baseline",
            ]),
            ("Root causes", [
                "Exit survey and win/loss themes",
                "Correlate with usage, support, NPS",
                "Distinguish preventable vs unavoidable",
            ]),
            ("Playbooks", [
                "Early warning triggers and actions",
                "Save offers and escalation paths",
                "Product gaps to feed PM",
            ]),
            ("Track interventions", [
                "Measure save rate of at-risk outreach",
                "Update health score model",
                "Report to leadership monthly",
            ]),
        ],
        "Analysis at `doc/customer-success/churn-<period>.md`.",
    ),
    "budget-plan": (
        "Budget Plan",
        "Build annual or quarterly budgets by department with assumptions and scenarios. Use for fiscal planning cycles.",
        [
            "Annual budget cycle kickoff",
            "Department budget submission",
            "Scenario planning for board review",
        ],
        [
            ("Gather inputs", [
                "Prior year actuals by cost center",
                "Headcount plan from HR",
                "Known commitments and contracts",
            ]),
            ("Build model", [
                "Separate Opex vs Capex",
                "Driver-based lines where possible",
                "Monthly phasing, not flat annual/12 only",
            ]),
            ("Scenarios", [
                "Base, upside, downside with triggers",
                "Document key assumptions",
                "Sensitivity on top 3 drivers",
            ]),
            ("Review", [
                "Reconcile to company targets",
                "Flag gaps requiring trade-offs",
                "Finance leadership approval before publish",
            ]),
        ],
        "Budget workbook and narrative at `doc/finance/budget-<fy>.md`.",
        "T2",
        "Not financial advice. For planning purposes only; requires qualified finance review.",
    ),
    "financial-forecast": (
        "Financial Forecast",
        "Create rolling financial forecasts updating actuals and projections. Use monthly or quarterly forecast cycles.",
        [
            "Monthly reforecast after close",
            "Mid-quarter outlook update for leadership",
            "Fundraising or board forecast refresh",
        ],
        [
            ("Actuals update", [
                "Import closed period actuals",
                "Explain variances vs prior forecast",
                "Adjust run-rate assumptions",
            ]),
            ("Projection", [
                "Revenue by stream with drivers",
                "Expense by category with ownership",
                "Cash timing for major items",
            ]),
            ("Risks and opportunities", [
                "List items that could move forecast ±X%",
                "Probability-weight if material",
                "Link to **variance-analysis**",
            ]),
            ("Communication", [
                "Executive summary of change vs last forecast",
                "Tables in **xlsx-analysis** format",
                "Version control forecast files",
            ]),
        ],
        "Forecast at `doc/finance/forecast-<period>.md`.",
        "T2",
        "Not financial advice. Projections are illustrative; actual results may differ materially.",
    ),
    "variance-analysis": (
        "Variance Analysis",
        "Analyze budget vs actual variances with narrative explanations and actions. Use after monthly close.",
        [
            "Monthly finance review with department heads",
            "Explaining miss to executive team",
            "Identifying corrective actions",
        ],
        [
            ("Calculate variances", [
                "Amount and % vs budget and vs prior year",
                "Split volume, price, timing effects where possible",
                "Materiality threshold for deep dive",
            ]),
            ("Explain drivers", [
                "One-time vs recurring",
                "Operational vs accounting timing",
                "Owner accountability per line item",
            ]),
            ("Actions", [
                "Corrective measures or forecast update",
                "Escalate structural gaps",
                "Celebrate favorable variances with caution",
            ]),
            ("Report", [
                "Waterfall chart narrative",
                "Forward-looking impact if trend continues",
                "Archive with close package",
            ]),
        ],
        "Report at `doc/finance/variance-<period>.md`.",
        "T2",
        "Not financial advice. Operational analysis only; confirm with finance systems of record.",
    ),
    "unit-economics": (
        "Unit Economics",
        "Model unit economics: CAC, LTV, margins, payback period. Use for SaaS or transactional business review.",
        [
            "Board or investor metrics review",
            "Pricing change impact analysis",
            "Go/no-go on new acquisition channel",
        ],
        [
            ("Define unit", [
                "Customer, order, or seat — consistent grain",
                "Time period for cohort analysis",
                "Gross vs net revenue definition",
            ]),
            ("Calculate metrics", [
                "CAC by channel; fully loaded vs marginal",
                "LTV with retention curve assumptions",
                "Contribution margin and payback months",
            ]),
            ("Sanity checks", [
                "Compare to industry benchmarks cautiously",
                "Stress test retention and CAC inflation",
                "Document formula alignment with finance",
            ]),
            ("Recommendations", [
                "Implications for spend and pricing",
                "Data gaps to improve accuracy",
                "No investment recommendations without advisor",
            ]),
        ],
        "Model at `doc/finance/unit-economics-<date>.md`.",
        "T2",
        "Not financial advice. Models use assumptions that must be validated by finance leadership.",
    ),
    "job-description-writer": (
        "Job Description Writer",
        "Write inclusive, accurate job descriptions with requirements and competencies. Use when opening new roles.",
        [
            "New requisition approved by HR",
            "Refreshing outdated JD for repost",
            "Creating role family template",
        ],
        [
            ("Role definition", [
                "Title aligned to leveling framework",
                "Team mission and reporting line",
                "Employment type and location policy",
            ]),
            ("Requirements", [
                "Must-have vs nice-to-have separated",
                "Competencies over years-of-experience proxy",
                "Inclusive language review per HR rule",
            ]),
            ("Sell the role", [
                "Impact statement and growth path",
                "Benefits summary pointer",
                "EEO and accommodation statement",
            ]),
            ("Approval", [
                "Hiring manager and HRBP sign-off",
                "Comp band attached in HRIS not public JD",
                "Post to approved channels only",
            ]),
        ],
        "JD at `doc/hr/jds/<role-id>.md`; publish via ATS.",
    ),
    "interview-kit-builder": (
        "Interview Kit Builder",
        "Build structured interview kits with stages, questions, and evaluation criteria. Use for consistent hiring loops.",
        [
            "New role interview loop design",
            "Calibration issues across interviewers",
            "Adding stage to existing loop",
        ],
        [
            ("Loop design", [
                "Stages: screen, technical, behavioral, final",
                "Interviewer roles and focus areas",
                "Time limits and rubric per stage",
            ]),
            ("Question bank", [
                "Behavioral questions linked to competencies",
                "Work sample or case if applicable",
                "Legal-safe questions only",
            ]),
            ("Evaluation", [
                "Link to **interview-scorecard**",
                "Debrief process and decision criteria",
                "Candidate experience touchpoints",
            ]),
            ("Packaging", [
                "Interviewer guide one-pager per stage",
                "Training note for new interviewers",
                "Store in ATS or shared drive",
            ]),
        ],
        "Kit at `doc/hr/interview-kits/<role-id>.md`.",
    ),
    "interview-scorecard": (
        "Interview Scorecard",
        "Create interview scorecards with rubrics for consistent candidate evaluation. Use for every interview stage.",
        [
            "After each interview completion",
            "Debrief preparation",
            "Calibration session input",
        ],
        [
            ("Rubric dimensions", [
                "3–5 competencies weighted for role",
                "1–4 scale definitions anchored with behaviors",
                "Separate culture add from culture fit cliché",
            ]),
            ("Evidence capture", [
                "Require specific examples cited",
                "Flag concerns vs strengths explicitly",
                "No protected-class notes",
            ]),
            ("Recommendation", [
                "Strong yes / yes / no / strong no",
                "Conditions: e.g. yes if reference confirms X",
                "Submit before debrief",
            ]),
            ("Debrief", [
                "Facilitator reads scorecards first",
                "Discuss divergence before vote",
                "Document decision and feedback to candidate",
            ]),
        ],
        "Scorecard in ATS; template at `doc/hr/scorecards/<role-id>.md`.",
    ),
    "onboarding-plan": (
        "Onboarding Plan",
        "Design 30-60-90 day onboarding plans for new hires. Use when offer accepted or internal transfer.",
        [
            "New employee start date confirmed",
            "Manager needs structured onboarding",
            "Role with long ramp (sales, enterprise AE)",
        ],
        [
            ("Pre-boarding", [
                "Equipment, access, welcome email schedule",
                "Buddy assignment",
                "Week 1 calendar draft",
            ]),
            ("30-60-90 goals", [
                "Learning, contribution, leadership phases",
                "Measurable outcomes per phase",
                "Checkpoints with manager and HR",
            ]),
            ("Resources", [
                "Required training and compliance",
                "Key people to meet matrix",
                "Documentation and tools access",
            ]),
            ("Feedback", [
                "Day 7 and day 30 pulse surveys",
                "Adjust plan based on role reality",
                "Close onboarding at 90-day review",
            ]),
        ],
        "Plan at `doc/hr/onboarding/<employee-id>.md` (PII-restricted access).",
    ),
    "sop-builder": (
        "SOP Builder",
        "Author standard operating procedures with RACI, steps, and exceptions. Use for repeatable operational processes.",
        [
            "New process needs documentation",
            "Audit finding requires SOP",
            "Scaling team beyond tribal knowledge",
        ],
        [
            ("Scope", [
                "Purpose, audience, and process owner",
                "Triggers that start the SOP",
                "Related SOPs and systems",
            ]),
            ("Procedure", [
                "Numbered steps with responsible role",
                "Inputs, outputs, and SLAs per step",
                "Screenshots or system paths if helpful",
            ]),
            ("Exceptions", [
                "Escalation paths and approvers",
                "Emergency bypass with post-review",
                "Revision history table",
            ]),
            ("Validate", [
                "Walkthrough with process performer",
                "Pilot before org-wide publish",
                "Annual review date on document",
            ]),
        ],
        "SOP at `doc/operations/sop/<process-id>.md`.",
    ),
    "process-optimization": (
        "Process Optimization",
        "Analyze and improve business processes using lean and value stream mapping. Use when cycle time or quality issues persist.",
        [
            "Process cycle time too long",
            "High error rate in handoffs",
            "Preparing for automation or scaling",
        ],
        [
            ("Current state map", [
                "Value stream from trigger to outcome",
                "Measure wait times and processing times",
                "Identify bottlenecks and rework loops",
            ]),
            ("Root cause", [
                "5-whys on top waste categories",
                "Distinguish policy vs execution issues",
                "Voice of customer/internal customer",
            ]),
            ("Future state", [
                "Eliminate, combine, automate, parallelize",
                "Define new RACI and metrics",
                "Estimate impact on time/cost/quality",
            ]),
            ("Implement", [
                "Pilot with one team",
                "Update **sop-builder** outputs",
                "Monitor KPIs for 90 days",
            ]),
        ],
        "Report at `doc/operations/process-improvement/<process>.md`.",
    ),
    "business-case": (
        "Business Case",
        "Build business cases with options, costs, benefits, and recommendation. Use for investment or change proposals.",
        [
            "Tool purchase or build proposal",
            "Headcount or org change request",
            "Process automation investment",
        ],
        [
            ("Problem statement", [
                "Current state cost or risk",
                "Stakeholders affected",
                "Strategic alignment",
            ]),
            ("Options analysis", [
                "Do nothing, minimum, recommended",
                "One-time and recurring costs",
                "Benefits: hard savings vs soft",
            ]),
            ("Financial summary", [
                "ROI, payback, NPV if data allows",
                "Sensitivity on key assumptions",
                "Not a substitute for finance sign-off",
            ]),
            ("Recommendation", [
                "Preferred option with risks",
                "Implementation timeline",
                "Success metrics at 90 days",
            ]),
        ],
        "Business case at `doc/operations/business-case-<initiative>.md`.",
    ),
    "status-report": (
        "Status Report",
        "Write RAG status reports for projects or operations with evidence and escalations. Use for weekly stakeholder updates.",
        [
            "Weekly project status to steering committee",
            "Operational KPI review",
            "Executive escalation needed",
        ],
        [
            ("Summary RAG", [
                "Overall and per dimension: scope, schedule, cost, risk",
                "One-line rationale per RAG color",
                "BLUF for executives",
            ]),
            ("Progress", [
                "Completed vs planned this period",
                "Upcoming milestones next period",
                "Dependencies on other teams",
            ]),
            ("Issues and decisions", [
                "Blockers with proposed resolution",
                "Decisions needed from audience",
                "RAID updates link",
            ]),
            ("Metrics", [
                "KPI table vs target",
                "Trend arrows and commentary",
                "Appendix for detail seekers",
            ]),
        ],
        "Report at `doc/operations/status/<project>-<date>.md`.",
    ),
    "raid-log": (
        "RAID Log",
        "Maintain risks, assumptions, issues, and dependencies log for programs. Use throughout program lifecycle.",
        [
            "Program kickoff setup",
            "Weekly program review",
            "Steerco prep needing risk visibility",
        ],
        [
            ("Structure log", [
                "Columns: ID, type, description, owner, impact, probability, status",
                "Separate risks (future) from issues (now)",
                "Dependencies with target dates",
            ]),
            ("Populate", [
                "Workshop initial RAID with team",
                "Add items from status reports and retros",
                "Retire closed items with resolution note",
            ]),
            ("Review cadence", [
                "Weekly owner updates",
                "Escalate red items to program sponsor",
                "Link mitigations to project plan",
            ]),
            ("Report", [
                "Top 5 risks for steerco",
                "Trend: new vs closed vs aged",
                "Connect to **program-status-report**",
            ]),
        ],
        "RAID log at `doc/program/raid-<program>.md` or tracker export.",
    ),
    "stakeholder-analysis": (
        "Stakeholder Analysis",
        "Map stakeholders by power, interest, and engagement strategy. Use at project or program start.",
        [
            "New program needing communication plan",
            "Conflict between stakeholder groups",
            "Change initiative rollout",
        ],
        [
            ("Identify stakeholders", [
                "Sponsors, users, blockers, dependencies",
                "Internal vs external",
                "Primary vs secondary",
            ]),
            ("Assess position", [
                "Power/interest grid placement",
                "Current attitude: supporter neutral critic",
                "Influence on success criteria",
            ]),
            ("Engagement plan", [
                "Communication frequency and channel",
                "Messages tailored per group",
                "RACI for decisions",
            ]),
            ("Maintain", [
                "Revisit after org changes",
                "Track sentiment shifts",
                "Document in **program-status-report**",
            ]),
        ],
        "Analysis at `doc/program/stakeholders-<initiative>.md`.",
    ),
    "program-status-report": (
        "Program Status Report",
        "Consolidated status across workstreams for program leadership. Use for monthly or steerco reporting.",
        [
            "Multi-project program review",
            "Steerco or board program update",
            "Cross-team dependency coordination",
        ],
        [
            ("Program snapshot", [
                "Objectives and benefits tracker",
                "Overall RAG with summary",
                "Budget and schedule at program level",
            ]),
            ("Workstream summaries", [
                "One paragraph per workstream lead",
                "Milestone heatmap",
                "Cross-dependencies status",
            ]),
            ("RAID highlights", [
                "Top risks and issues from **raid-log**",
                "Decisions needed this period",
                "Escalations with options",
            ]),
            ("Benefits and next period", [
                "Benefits realized vs plan",
                "Focus for next reporting period",
                "Appendix for detailed metrics",
            ]),
        ],
        "Report at `doc/program/status-<program>-<date>.md`.",
    ),
    "contract-review-checklist": (
        "Contract Review Checklist",
        "Operational checklist for commercial contract review — not legal advice. Use when triaging contracts before counsel review.",
        [
            "Sales or procurement received customer/vendor contract",
            "Renewal with changed terms",
            "Standard vs non-standard contract triage",
        ],
        [
            ("Identify contract type", [
                "MSA, SOW, DPA, license, NDA cross-ref",
                "Jurisdiction and governing law noted",
                "Business owner and deadline",
            ]),
            ("Checklist review", [
                "Parties, term, termination, auto-renewal",
                "Liability caps, indemnity, warranty",
                "Payment terms, SLAs, IP ownership",
                "Data protection and security addendum",
            ]),
            ("Flag non-standard", [
                "Mark clauses deviating from playbook",
                "Risk rating: low/medium/high for counsel",
                "Never recommend sign/reject — escalate",
            ]),
            ("Handoff", [
                "Package checklist + redlines for legal",
                "Track status in CLM",
                "Archive approved playbook updates",
            ]),
        ],
        "Checklist at `doc/legal/contract-review-<id>.md`.",
        "T3",
        "This checklist is for operational triage only and does not constitute legal advice. Consult qualified counsel for binding decisions.",
    ),
    "nda-triage": (
        "NDA Triage",
        "Triage mutual and one-way NDAs against standard templates — not legal advice. Use before sending to legal counsel.",
        [
            "Prospect or partner sent NDA for signature",
            "Outbound NDA before sharing confidential info",
            "NDA expired needs renewal check",
        ],
        [
            ("Classify NDA", [
                "Mutual vs one-way; purpose stated",
                "Term and survival of confidentiality",
                "Standard template vs third-party paper",
            ]),
            ("Key clauses", [
                "Definition of confidential information",
                "Exclusions: public, prior knowledge, independent dev",
                "Permitted disclosures and compulsion",
                "Return/destroy obligations",
            ]),
            ("Red flags", [
                "Non-solicit, non-compete buried in NDA",
                "Overbroad IP assignment",
                "Unlimited liability or missing cap",
                "Non-standard jurisdiction",
            ]),
            ("Route", [
                "Green: matches approved template → legal quick review",
                "Yellow: minor edits → legal full review",
                "Red: material issues → legal negotiation required",
            ]),
        ],
        "Triage note at `doc/legal/nda-triage-<counterparty>.md`.",
        "T3",
        "This triage is for operational routing only and does not constitute legal advice. Only authorized signatories may execute NDAs.",
    ),
    "strategic-planning": (
        "Strategic Planning",
        "Facilitate strategic planning with vision, pillars, OKRs, and initiatives. Use for annual or multi-year planning cycles.",
        [
            "Annual strategy offsite preparation",
            "Refresh strategy after market shift",
            "Aligning departments to corporate strategy",
        ],
        [
            ("Situation assessment", [
                "Run **swot-analysis** and market context",
                "Review performance vs prior strategy",
                "Stakeholder input synthesis",
            ]),
            ("Strategic choices", [
                "Where to play / how to win framing",
                "3–5 strategic pillars max",
                "Explicit choices and trade-offs",
            ]),
            ("OKRs and initiatives", [
                "Company OKRs cascading guidance",
                "Initiative portfolio mapped to pillars",
                "Resource implications high-level",
            ]),
            ("Communication", [
                "Strategy on a page for all-hands",
                "Leader talking points",
                "Quarterly review cadence defined",
            ]),
        ],
        "Strategy doc at `doc/strategy/plan-<year>.md`.",
    ),
    "swot-analysis": (
        "SWOT Analysis",
        "Conduct SWOT analysis with actionable strategies from TOWS matrix. Use for strategic or product positioning decisions.",
        [
            "Strategy session input",
            "Entering new market assessment",
            "Competitive repositioning",
        ],
        [
            ("Gather inputs", [
                "Internal data: strengths/weaknesses evidence",
                "External: opportunities/threats from research",
                "Cross-functional workshop participants",
            ]),
            ("Populate SWOT", [
                "Specific bullets, not generic platitudes",
                "Prioritize top 3 per quadrant",
                "Link to **competitive-landscape** if needed",
            ]),
            ("TOWS strategies", [
                "SO: use strengths on opportunities",
                "WO: fix weaknesses to capture opportunities",
                "ST: strengths against threats",
                "WT: defensive priorities",
            ]),
            ("Actions", [
                "Convert top strategies to initiatives",
                "Owners and timelines",
                "Review triggers quarterly",
            ]),
        ],
        "Analysis at `doc/strategy/swot-<topic>.md`.",
    ),
    "competitive-landscape": (
        "Competitive Landscape",
        "Map competitive landscape with segments, players, and strategic implications. Use for strategy and executive briefings.",
        [
            "Board or investor competitive overview",
            "Market entry decision support",
            "Annual strategy refresh",
        ],
        [
            ("Define market scope", [
                "Segment definition and sizing sources",
                "Direct vs adjacent competitors",
                "Customer alternatives including status quo",
            ]),
            ("Profile players", [
                "Positioning, pricing, strengths, weaknesses",
                "Recent moves: funding, product, M&A",
                "Win/loss themes if available",
            ]),
            ("Implications", [
                "White space and differentiation opportunities",
                "Threats to monitor",
                "Do not duplicate **technology-scouting** depth — link instead",
            ]),
            ("Executive summary", [
                "2-page max main narrative",
                "Landscape map visual",
                "Recommended strategic responses",
            ]),
        ],
        "Report at `doc/strategy/competitive-landscape-<date>.md`.",
    ),
    "internal-comms": (
        "Internal Comms",
        "Draft internal communications for org announcements, change, and updates. Use for all-hands, reorgs, or policy changes.",
        [
            "Major org or leadership announcement",
            "Product or policy change affecting employees",
            "Crisis internal holding message",
        ],
        [
            ("Audience segmentation", [
                "All hands vs affected teams vs managers",
                "Regions and languages if needed",
                "Manager talking points separate if sensitive",
            ]),
            ("Message structure", [
                "What is changing, why, when, what employees do",
                "Link FAQ and feedback channel",
                "Acknowledge uncertainty honestly",
            ]),
            ("Channel plan", [
                "Email, Slack, town hall sequencing",
                "Timing: avoid holidays; manager preview first",
                "Follow-up cadence for evolving situations",
            ]),
            ("Approval", [
                "Comms + HR + legal for sensitive topics",
                "Track questions for FAQ updates",
                "Measure readership if platform supports",
            ]),
        ],
        "Draft at `doc/comms/internal/<topic>.md`.",
    ),
    "rfp-draft": (
        "RFP Draft",
        "Draft request for proposal documents for vendor selection. Use when formal sourcing process required.",
        [
            "New vendor category needs competitive bid",
            "Contract renewal with RFP requirement",
            "Public sector or enterprise procurement policy",
        ],
        [
            ("Requirements", [
                "Business and technical requirements",
                "Mandatory vs scored criteria",
                "Integration and security requirements",
            ]),
            ("RFP structure", [
                "Timeline, submission format, questions process",
                "Pricing template and TCO instructions",
                "Legal terms reference or attachment",
            ]),
            ("Evaluation plan", [
                "Weighted scoring matrix shared with evaluators",
                "Demo or POC phase if needed",
                "Conflict of interest declarations",
            ]),
            ("Publish and manage", [
                "Issue to approved vendor list",
                "Q&A log shared with all bidders",
                "Hand responses to **vendor-evaluation**",
            ]),
        ],
        "RFP at `doc/procurement/rfp-<project>.md`.",
    ),
    "vendor-evaluation": (
        "Vendor Evaluation",
        "Evaluate vendor proposals with weighted scoring and recommendation. Use after RFP responses or PoC completion.",
        [
            "RFP responses received",
            "Vendor shortlist demo scoring",
            "Renewal vs switch analysis",
        ],
        [
            ("Scoring setup", [
                "Criteria weights from RFP",
                "Evaluators independent scores first",
                "Reference checks for finalists",
            ]),
            ("Compare proposals", [
                "Feature fit, price, TCO, risk",
                "Security and compliance questionnaire",
                "Implementation timeline and support",
            ]),
            ("Recommendation", [
                "Preferred vendor with rationale",
                "Negotiation levers identified",
                "Backup vendor if primary fails",
            ]),
            ("Document", [
                "Retain scoring worksheets per policy",
                "Route to procurement and legal for contract",
                "Link **technology-scouting** for tech depth if needed",
            ]),
        ],
        "Evaluation at `doc/procurement/vendor-eval-<project>.md`.",
    ),
})
