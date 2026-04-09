# Development Plan — Fabric Brain

> Guidelines for evolving, extending, and maintaining the Brain.

---

## 1. Adding a New Agent

### Criteria

Add a new agent when **all 3** conditions are met:
1. The domain owns **3+ distinct files** or **1 complex deployment script**
2. The domain has **domain-specific gotchas** not covered by existing agents
3. At least **2 workflows** would benefit from the agent's existence

### Scaffolding Checklist

```
agents/{agent-name}/
├── README.md           ← From template below
├── instructions.md     ← System prompt
├── known_issues.md     ← Start empty, populate as discovered
└── SPEC.md             ← Formal interface (see SPEC template)
```

### README Template

```markdown
# {Agent Name}

> **Version**: 1.0  
> **Category**: {Data Eng | Analytics | Platform | RTI | Migration | Meta}  
> **Invoke when**: {one-line trigger description}

## What This Agent Owns

| Resource | Scope |
|----------|-------|
| ... | ... |

## What This Agent Does NOT Own

- Item X → use `other-agent`

## Files

| File | Purpose |
|------|---------|
| instructions.md | System prompt — LOAD FIRST |
| known_issues.md | Gotchas and workarounds |
| SPEC.md | Formal interface specification |

## Quick Start

1. Read `instructions.md`
2. Read project config
3. Execute task within scope

## Key Insight

> "One critical sentence about this domain."
```

### Registration

After creating agent files:
1. Add entry to `AGENTS.md` quick reference table (§ Quick Reference)
2. Add to category section in `AGENTS.md` (§ Agent Categories)
3. Update item coverage table in `PROJECT_PLAN.md`
4. Add to relevant workflows in `WORKFLOWS.md` if applicable

---

## 2. Modifying an Agent

### Rules

- **Only the owning agent modifies its own files** (see AGENTS.md § File Ownership)
- **Brain-level files** require project-orchestrator (01) ownership check
- **Cross-agent changes** (touching 2+ agents) go through project-orchestrator

### Change Process

1. Read `instructions.md` and `known_issues.md` of the target agent
2. Make focused changes within scope
3. Update `known_issues.md` if new gotcha discovered
4. If the change affects other agents, document the impact in the handoff

---

## 3. SPEC.md Template

Every agent should have a `SPEC.md` in its folder. Use this template:

```markdown
# {Agent Name} — Technical Specification

> Version: 1.0

## Identity

- **Agent**: {name}
- **Category**: {category}
- **Owner**: This agent is the sole owner of all files in this folder.

## Inputs

| Input | Source | Format | Required |
|-------|--------|--------|----------|
| Project config | orchestrator (01) | YAML | Yes |
| ... | ... | ... | ... |

## Outputs

| Output | Consumer | Format |
|--------|----------|--------|
| Item ID | resource_ids.md | GUID string |
| ... | ... | ... |

## Constraints

1. {Hard constraint — e.g., "MUST use Legacy PBIX format"}
2. {Hard constraint — from shared_constraints.md}
3. {Domain-specific constraint}

## Delegation

| When this happens | Delegate to |
|-------------------|-------------|
| Need Delta tables first | lakehouse-agent (05) |
| ... | ... |

## Error Handling

| Error Pattern | Action |
|---------------|--------|
| HTTP 429 | Retry with exponential backoff |
| HTTP 404 on item | Item deleted — recreate |
| ... | ... |

## Validation

After execution, verify:
- [ ] Item exists in workspace (GET returns 200)
- [ ] Item renders correctly in portal
- [ ] Resource ID stored in config/state
```

---

## 4. Testing Strategy

### Per-Agent Testing

Each agent should be testable independently:
1. **Smoke test**: Can the agent create its primary artifact?
2. **Idempotency test**: Running twice produces the same result
3. **Handoff test**: Output matches what the consuming agent expects

### Cross-Agent Testing (Workflows)

The 5 workflows in `WORKFLOWS.md` serve as integration tests:
1. Standard BI Demo — workspace → model → report → agent
2. RTI Demo — workspace → eventhouse → eventstream → dashboard
3. Smart Factory — workspace → lakehouse → eventhouse → graph
4. Data Agent — workspace → lakehouse → model → agent → evaluate
5. BO Migration — assessment → mapping → generation → validation

### Validation Approach

For now, testing is **manual + script-driven**:
- Deploy scripts are idempotent (safe to re-run)
- `state.json` tracks what was created
- Known issues are documented per-agent
- AI Skills Analysis Agent (12) provides automated evaluation for Data Agent workflows

---

## 5. Backward Compatibility

### Policy

- **Knowledge files**: Non-breaking — always additive
- **Instructions changes**: May change agent behavior — test after update
- **AGENTS.md changes**: Must keep quick reference table up-to-date
- **Workflow changes**: Must notify all agents in the workflow chain

### Deprecation Process

1. Mark agent/file as deprecated in README
2. Add migration note pointing to replacement
3. Keep deprecated agent for 2 versions
4. Remove after confirming no workflows reference it

---

## 6. Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Agent folder | `{domain}-agent` | `lakehouse-agent` |
| Agent with sub-focus | `{domain}-{focus}-agent` | `ai-skills-analysis-agent` |
| Knowledge file | `{topic}.md` or `{topic}_*.md` | `kql_query_patterns.md` |
| Deploy script | `deploy_{item_type}.py` | `deploy_semantic_model.py` |
| Template | `template_{name}.md` | `template_star_schema.yaml` |
| Config | `config.yaml` | — |
| State tracking | `state.json` | — |

---

## 7. Contributing

### Adding Knowledge to an Existing Agent

1. Identify the owning agent (see AGENTS.md § File Ownership)
2. Add content to the most relevant existing file
3. If no file fits, create a new `.md` file in the agent folder
4. Update the agent's README files table

### Reporting a Known Issue

1. Add to the relevant agent's `known_issues.md`
2. If cross-cutting, add to brain-level `known_issues.md`
3. Include: **symptom**, **cause**, **workaround**, **status** (open/fixed)

### Proposing a New Workflow

1. Define the agent sequence with phases and gates
2. Specify inputs/outputs per phase
3. Add to `WORKFLOWS.md`
4. Update `TEMPLATES.md` if it creates a reusable project pattern
