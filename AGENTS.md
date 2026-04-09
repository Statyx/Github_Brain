# Multi-Agent Architecture — Fabric Brain

## Quick Reference

| # | Agent | Category | Invoke When | Owns |
|----|-------|----------|-------------|------|
| 01 | **project-orchestrator-agent** | Meta | New project kickoff, multi-step build | `config_templates.md`, naming, 12-step pipeline |
| 02 | **project-presentation-agent** | Meta | README scaffolding, repo structure, badges | README patterns, community files |
| 03 | **workspace-admin-agent** | Platform | Workspace CRUD, capacity, RBAC, Git | `agents/workspace-admin-agent/` |
| 04 | **domain-modeler-agent** | Data Eng | Star schema design, industry templates, data gen | `agents/domain-modeler-agent/` |
| 05 | **lakehouse-agent** | Data Eng | OneLake, Delta tables, Spark, SQL Endpoint | `agents/lakehouse-agent/` |
| 06 | **warehouse-agent** | Data Eng | T-SQL DW, CTAS, COPY INTO, stored procs | `agents/warehouse-agent/` |
| 07 | **dataflow-agent** | Data Eng | Dataflow Gen2, Power Query M, destinations | `agents/dataflow-agent/` |
| 08 | **orchestrator-agent** | Data Eng | Pipelines, notebooks, copy jobs, scheduling | `agents/orchestrator-agent/` |
| 09 | **semantic-model-agent** | Analytics | DAX, relationships, model.bim, Direct Lake, TMDL | `agents/semantic-model-agent/` |
| 10 | **report-builder-agent** | Analytics | Power BI visuals, pages, themes (Legacy PBIX) | `agents/report-builder-agent/` |
| 11 | **ai-skills-agent** | Analytics | Data Agents, AI instructions, few-shots | `agents/ai-skills-agent/` |
| 12 | **ai-skills-analysis-agent** | Analytics | Agent evaluation, DAX quality, RCA, diagnostics | `agents/ai-skills-analysis-agent/` |
| 13 | **rti-eventstream-agent** | RTI | EventStreams, routing, Event Hub SDK | `agents/rti-eventstream-agent/` |
| 14 | **rti-kusto-agent** | RTI | Eventhouse, KQL databases, KQL dashboards | `agents/rti-kusto-agent/` |
| 15 | **ontology-agent** | RTI | Entity types, graph models, GQL queries | `agents/ontology-agent/` |
| 16 | **fabric-cli-agent** | Platform | `fab` CLI, item management, CI/CD | `agents/fabric-cli-agent/` |
| 17 | **cicd-fabric-agent** | Platform | Git integration, deployment pipelines, env promotion | `agents/cicd-fabric-agent/` |
| 18 | **monitoring-agent** | Platform | Job tracking, capacity monitoring, audit logs | `agents/monitoring-agent/` |
| 19 | **taskflow-agent** | Platform | Task Flow design, templates, JSON import/export | `agents/taskflow-agent/` |
| 20 | **extensibility-toolkit-agent** | Platform | Fabric Workload SDK, iFrame, manifest, publishing | `agents/extensibility-toolkit-agent/` |
| 21 | **migration-bo-agent** | Migration | SAP BO → Fabric, 119 DAX mappings, 78 visual maps | `agents/migration-bo-agent/` |
| 22 | **architecture-design-agent** | Meta | Architecture diagrams, SVG icons, Draw.io libraries | `agents/architecture-design-agent/` |

---

## 1. Architecture Overview

The Fabric Brain is a **22-agent knowledge system** coordinated by a central **project-orchestrator-agent**. Each agent owns one Fabric domain end-to-end and exposes knowledge via a consistent file structure.

```
                          ┌──────────────────────────┐
                          │  project-orchestrator (01)│
                          │  12-step config pipeline  │
                          └────────────┬─────────────┘
                                       │
         ┌────────────┬────────────┬───┴───┬────────────┬────────────┐
         │            │            │       │            │            │
   ┌─────▼──────┐ ┌───▼────┐ ┌────▼───┐ ┌─▼──────┐ ┌──▼───────┐ ┌─▼──────────┐
   │  workspace  │ │ domain │ │  lake  │ │semantic│ │  report  │ │ ai-skills  │
   │  admin (03) │ │modeler │ │house   │ │ model  │ │ builder  │ │  agent(11) │
   │             │ │  (04)  │ │  (05)  │ │  (09)  │ │  (10)    │ │            │
   └─────────────┘ └────────┘ └────────┘ └────────┘ └──────────┘ └────────────┘
         │                       │           │            │
   ┌─────▼──────┐          ┌────▼───┐  ┌────▼───┐  ┌─────▼─────┐
   │  cicd (17) │          │  orch  │  │security│  │ analysis  │
   │  fabric    │          │  (08)  │  │  (TBD) │  │   (12)    │
   └────────────┘          └────────┘  └────────┘  └───────────┘
```

---

## 2. Agent Communication Model

### 2.1 Coordination Pattern

Agents communicate via **explicit handoff** — no shared mutable state. Each handoff includes:
- Artifact names and IDs produced
- File paths written
- Next agent to invoke
- Input data the next agent needs

All coordination metadata lives in **project config files** (YAML/JSON) and **`resource_ids.md`** — not in external services.

### 2.2 Agent Interface Contract

Every agent exposes a consistent knowledge structure:

```
agents/{agent-name}/
├── README.md           ← Identity, scope, ownership, handoff targets
├── instructions.md     ← System prompt (LOAD FIRST), mandatory rules, decision trees
├── known_issues.md     ← Gotchas, debugging checklist, workarounds
├── SPEC.md             ← Formal interface: inputs, outputs, constraints, delegation
├── {topic}_*.md        ← Domain-specific knowledge files (variable count)
└── templates/          ← Ready-to-use scripts and configs (optional)
```

### 2.3 Agent Lifecycle

```
  SESSION START → LOAD instructions.md → READ config → PLAN → EXECUTE → VALIDATE → HANDOFF
                                                         │                    │
                                                         └──► FAIL ──► ERROR_RECOVERY.md
```

---

## 3. Agent Categories

### Meta / Orchestration & Visualization (3 agents)

**project-orchestrator-agent (01)**: 12-step config-driven pipeline that coordinates all other agents. Owns project-level configs, naming conventions, and state management.

**project-presentation-agent (02)**: README scaffolding, repo structure, badges, community files. Invoked at the end to polish project presentation.

**architecture-design-agent (22)**: Architecture diagram generation using 303 official Microsoft Fabric & Azure SVG icons. Produces Mermaid, Draw.io, and SVG composition diagrams for solution architecture, data flow, and deployment topology.

### Data Engineering (5 agents)

**domain-modeler-agent (04)**: Star schema design from industry templates. Produces YAML model specs, CSV sample data, and cross-layer output (Delta schemas + KQL schemas + DAX measure definitions).

**lakehouse-agent (05)**: OneLake DFS operations, Delta tables, Spark notebooks, SQL Endpoint provisioning. Owns the physical data layer.

**warehouse-agent (06)**: T-SQL Data Warehouse authoring — CTAS, COPY INTO, transactions, time travel, stored procedures.

**dataflow-agent (07)**: Dataflow Gen2 (Power Query M), data destinations, incremental refresh patterns.

**orchestrator-agent (08)**: Fabric Data Factory pipelines, notebooks, copy activities, ForEach patterns, scheduling.

### Analytics & Reporting (4 agents)

**semantic-model-agent (09)**: DAX measures, relationships, model.bim deployment, Direct Lake, TMDL/getDefinition, Prep for AI annotations.

**report-builder-agent (10)**: Power BI report creation using **Legacy PBIX format ONLY**. Visual catalog, page layout, themes, prototypeQuery.

**ai-skills-agent (11)**: Data Agent creation — 7-section AI instruction framework, few-shot examples, datasource binding, thread management.

**ai-skills-analysis-agent (12)**: Data Agent evaluation — 24 BPA rules, DAX quality scoring, root cause analysis, diagnostic JSON schema.

### Real-Time Intelligence (3 agents)

**rti-eventstream-agent (13)**: EventStream topology, routing rules, custom endpoints, Event Hub SDK injection.

**rti-kusto-agent (14)**: Eventhouse, KQL databases, streaming ingestion, KQL dashboards, materialized views. Richest agent (12 files).

**ontology-agent (15)**: Entity type modeling, graph models, GQL queries (ISO/IEC 39075), data bindings.

### Platform & Operations (5 agents)

**fabric-cli-agent (16)**: `fab` CLI command reference, item management, CI/CD deploy patterns.

**cicd-fabric-agent (17)**: Git integration, deployment pipelines, variable libraries, environment promotion (dev → test → prod).

**monitoring-agent (18)**: Job tracking, capacity monitoring, audit logs, Admin APIs, KQL observability dashboards.

**taskflow-agent (19)**: Task Flow design, templates, JSON import/export, item assignment.

**extensibility-toolkit-agent (20)**: Fabric Workload Development Kit, iFrame SDK, manifest authoring, component library, remote hosting.

### Migration (1 agent)

**migration-bo-agent (21)**: SAP BusinessObjects → Fabric migration. 119 BO→DAX expression mappings, 78 visual type mappings, assessment framework, migration playbook.

### Visualization (1 agent)

**architecture-design-agent (22)**: Architecture diagram generation using 303 official Microsoft Fabric & Azure SVG icons (7 categories: Azure Core, Azure DevOps, Fabric Artifacts, Fabric Black, Fabric Core, Fabric Datasources, Microsoft Tools). Supports Mermaid, Draw.io XML, and SVG composition. Icons sourced from [astrzala/FabricToolset](https://github.com/astrzala/FabricToolset).

---

## 4. Data Flow Between Agents

### Standard BI Demo Workflow

```
  project-orchestrator (01)
    │
    ├─► workspace-admin (03)     → Workspace ID
    ├─► domain-modeler (04)      → YAML model + CSVs + DAX definitions
    ├─► lakehouse-agent (05)     → Lakehouse ID + Delta tables
    ├─► semantic-model-agent (09)→ Semantic Model ID + model.bim
    ├─► report-builder (10)      → Report ID + visuals
    ├─► ai-skills-agent (11)     → Data Agent ID (optional)
    └─► project-presentation (02)→ README + badges
```

### RTI Demo Workflow

```
  project-orchestrator (01)
    │
    ├─► workspace-admin (03)     → Workspace ID
    ├─► domain-modeler (04)      → KQL schemas + ontology + CSVs
    ├─► rti-kusto-agent (14)     → Eventhouse + KQL DB + tables
    ├─► rti-eventstream-agent (13)→ EventStream + routing
    ├─► ontology-agent (15)      → Graph model (optional)
    ├─► semantic-model-agent (09)→ Semantic Model (optional)
    └─► report-builder (10)      → KQL Dashboard or PBI Report
```

> **Full workflow details**: See `WORKFLOWS.md` for 5 complete end-to-end sequences with validation gates.

---

## 5. File Ownership Rules

### Principles
- **One owner per file** — each knowledge file has exactly one owning agent
- **Read access is universal** — any agent can read any file for context
- **Write access is restricted** — only the owning agent modifies its files
- **Brain-level files** — owned by project-orchestrator-agent (01) unless stated otherwise

### Brain-Level Knowledge Files

| File | Owner | Purpose |
|------|-------|---------|
| `agent_principles.md` | project-orchestrator (01) | Operating principles for all agents |
| `shared_constraints.md` | project-orchestrator (01) | 8 hard rules for all agents |
| `fabric_api.md` | project-orchestrator (01) | REST API patterns, auth, LRO |
| `environment.md` | workspace-admin (03) | Python, Azure CLI, PowerShell setup |
| `resource_ids.md` | workspace-admin (03) | GUIDs, endpoints, connection strings |
| `known_issues.md` | project-orchestrator (01) | Cross-cutting gotchas |
| `report_format.md` | report-builder (10) | Legacy PBIX format spec |
| `visual_builders.md` | report-builder (10) | Visual config, expression language |
| `semantic_model.md` | semantic-model (09) | model.bim, Direct Lake, TMDL |
| `onelake.md` | lakehouse (05) | DFS API 3-step upload protocol |
| `warehouse_patterns.md` | warehouse (06) | T-SQL DW authoring |
| `spark_patterns.md` | lakehouse (05) | Spark/Lakehouse patterns |
| `item_definitions.md` | project-orchestrator (01) | Definition envelope for 20+ item types |
| `mcp_powerbi.md` | semantic-model (09) | MCP Power BI tools (21 tools) |
| `mcp_registry.md` | project-orchestrator (01) | MCP Server Registry (7 servers) |
| `mirrored_databases.md` | lakehouse (05) | Mirrored DB patterns, CDC sync |
| `WORKFLOWS.md` | project-orchestrator (01) | 5 cross-agent workflow sequences |
| `TEMPLATES.md` | project-orchestrator (01) | 5 project templates with checklists |
| `ERROR_RECOVERY.md` | project-orchestrator (01) | Decision trees by HTTP status |

---

## 6. Handoff Protocol

When an agent completes its phase and transitions to another:

1. **Complete your part** — finish everything within your file scope
2. **State the handoff** — clearly describe what was produced
3. **Name the target agent** — e.g., "Hand off to semantic-model-agent (09) for model.bim"
4. **List artifacts** — specify IDs, file paths, and config keys
5. **Include context** — provide any intermediate results the next agent needs

### Example Handoff

```
lakehouse-agent (05) → semantic-model-agent (09):
  "Lakehouse provisioned. Delta tables created for all 7 tables.
   Lakehouse ID: fa2333c4-b003-440b-b6f5-25b6e2454d6c
   SQL Endpoint: abc123.datawarehouse.fabric.microsoft.com
   Tables: dim_countries, dim_disciplines, dim_wbs, dim_norms,
           dim_escalation, fact_benchmarks, fact_estimates
   Row counts verified. Ready for model.bim generation."
```

---

## 7. Shared Infrastructure

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Language | Python 3.12+ | Fabric SDK, async I/O, Pydantic models |
| API Client | `requests` + Azure Identity | Token management, retry logic |
| Config Format | YAML (project) + JSON (Fabric API) | Human-readable + API-compatible |
| State | `resource_ids.md` + `state.json` | Flat files, no external services |
| Auth | Azure CLI credential (`DefaultAzureCredential`) | Works locally + CI/CD |
| Deployment | Fabric REST API (async LRO) | Idempotent create-or-update |
| Reports | Legacy PBIX format | Only format that renders visuals correctly |
| Semantic Models | model.bim (V3) or TMDL | Direct Lake, entity partitions |

---

## 8. When NOT to Use Specialized Agents

Use the **project-orchestrator-agent (01)** or general Brain context for:
- Quick questions about Fabric APIs or patterns
- Multi-domain tasks that touch 3+ agents simultaneously
- Documentation updates (CHANGELOG, README, etc.)
- Git operations (commit, push)
- Infrastructure changes (capacity, permissions)

---

## 9. Key References

| Document | Path | Purpose |
|----------|------|---------|
| Agent SPECs | `agents/*/SPEC.md` | Per-agent technical specifications |
| Shared Constraints | `shared_constraints.md` | 8 hard rules for all agents |
| Operating Principles | `agent_principles.md` | How agents think and act |
| Workflows | `WORKFLOWS.md` | 5 end-to-end cross-agent sequences |
| Templates | `TEMPLATES.md` | 5 project templates with checklists |
| Error Recovery | `ERROR_RECOVERY.md` | Decision trees by HTTP status |
| Known Issues | `known_issues.md` | Cross-cutting gotchas |
| Environment | `environment.md` | Setup requirements |
