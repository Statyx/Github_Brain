# Project Plan — Fabric Brain v2.0

> Roadmap for evolving the 21-agent knowledge system.

---

## Current State (v1.x)

- **21 agents** across 6 categories (Meta, Data Eng, Analytics, RTI, Platform, Migration)
- **20 knowledge files** at brain-level
- **5 workflows** end-to-end (Standard BI, RTI, Smart Factory, Data Agent, BO Migration)
- **5 templates** with checklists and time estimates
- Proven in production: CCE_Advisor (92%), Fabric RTI Demo, Financial_Platform

### Strengths
- Consistent per-agent file structure (README, instructions, known_issues)
- Strong shared constraints (8 hard rules) and operating principles (6 principles)
- Config-driven, idempotent deployment patterns
- Rich domain knowledge (Kusto agent = 12 files, BO migration = 119 DAX mappings)

### Gaps (identified via OACToFabric comparison)
- No master registry → AGENTS.md (✅ created)
- No formal per-agent specs → SPEC.md (planned)
- No file ownership mapping → AGENTS.md §5 (✅ created)
- No semantic versioning for the Brain itself
- No automated test/validation framework
- No coverage tracking (which Fabric item types have agents?)

---

## Fabric Item Type Coverage

| Item Type | Agent | Status |
|-----------|-------|--------|
| Workspace | workspace-admin (03) | ✅ Covered |
| Lakehouse | lakehouse (05) | ✅ Covered |
| Warehouse | warehouse (06) | ✅ Covered |
| Semantic Model | semantic-model (09) | ✅ Covered |
| Report (PBI) | report-builder (10) | ✅ Covered |
| Data Agent | ai-skills (11) | ✅ Covered |
| EventStream | rti-eventstream (13) | ✅ Covered |
| Eventhouse / KQL DB | rti-kusto (14) | ✅ Covered |
| KQL Dashboard | rti-kusto (14) | ✅ Covered |
| Notebook | lakehouse (05) / orchestrator (08) | ✅ Shared |
| Pipeline | orchestrator (08) | ✅ Covered |
| Dataflow Gen2 | dataflow (07) | ✅ Covered |
| Deployment Pipeline | cicd-fabric (17) | ✅ Covered |
| Task Flow | taskflow (19) | ✅ Covered |
| Mirrored Database | lakehouse (05) | ✅ Covered |
| Shortcut | lakehouse (05) | ⚠️ Partial |
| Paginated Report | — | ❌ No agent |
| ML Model / Experiment | — | ❌ No agent |
| Reflex (Data Activator) | — | ❌ No agent |
| GraphQL API | — | ❌ No agent |
| Copy Job | orchestrator (08) | ⚠️ Partial |
| Environment | — | ❌ No agent |
| Architecture Diagrams | architecture-design (22) | ✅ Covered |

---

## Roadmap

### Phase 1: Formalization (Current)
- [x] AGENTS.md — Master registry with quick reference, ownership, handoff protocol
- [ ] SPEC.md — Create template and apply to 1 pilot agent
- [ ] DEV_PLAN.md — Evolution strategy, contribution guidelines
- [ ] Semantic versioning: Tag Brain as v1.0 (current), v2.0 (formalized)

### Phase 2: Coverage Expansion
- [ ] **ml-experiment-agent** — ML models, experiments, MLflow, AutoML in Fabric
- [ ] **graphql-agent** — GraphQL API items, schema, resolvers, auth
- [ ] **reflex-agent** — Data Activator triggers, reflexes, alert rules
- [ ] **environment-agent** — Spark environments, library management, R/Python
- [ ] **shortcut-agent** — OneLake shortcuts, S3/ADLS/GCS cross-cloud shortcuts

### Phase 3: Cross-Agent Intelligence
- [ ] **Automated workflow testing** — Validate 5 workflows end-to-end
- [ ] **Agent self-improvement loop** — Agents can propose updates to their own files
- [ ] **Knowledge graph** — Map dependencies between agents, files, and Fabric APIs
- [ ] **Template generator** — Auto-scaffold new agent folders from SPEC.md template

### Phase 4: Advanced Capabilities
- [ ] **Multi-workspace orchestration** — Cross-workspace pipelines, shared semantic models
- [ ] **Capacity optimization agent** — Right-sizing, CU monitoring, throttling response
- [ ] **Data governance agent** — Sensitivity labels, endorsement, lineage, purview integration
- [ ] **Cost estimation agent** — Pre-deployment cost modeling for Fabric SKUs

---

## Versioning Strategy

| Version | Description |
|---------|-------------|
| v1.0 | Current state — 21 agents, informal structure |
| v1.1 | Formalization complete (AGENTS.md, DEV_PLAN.md, SPEC.md template) |
| v2.0 | All agents have SPEC.md + 25+ item types covered |
| v3.0 | Automated testing + self-improvement loop active |

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2025-01 | Legacy PBIX for reports | Only format that renders visuals correctly |
| 2025-02 | model.bim V3 over TMDL | Simpler single-file deployment |
| 2025-03 | 3-layer Data Agent model | Orchestrator/DAX Tool/Response separation |
| 2025-04 | OACToFabric-inspired formalization | Master registry, SPEC.md, file ownership |
