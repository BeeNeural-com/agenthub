---
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
