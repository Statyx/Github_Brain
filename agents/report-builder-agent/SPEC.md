# report-builder-agent — Technical Specification

> Version: 1.0

## Identity

- **Agent**: report-builder-agent (#10)
- **Category**: Analytics & Reporting
- **Owner**: Sole owner of all files in `agents/report-builder-agent/`
- **Brain-level ownership**: `report_format.md`, `visual_builders.md`

## Inputs

| Input | Source | Format | Required |
|-------|--------|--------|----------|
| Workspace ID | workspace-admin (03) via `resource_ids.md` | GUID | Yes |
| Semantic Model ID | semantic-model (09) via `resource_ids.md` | GUID | Yes |
| Model schema (tables, columns, measures) | semantic-model (09) via model.bim | JSON | Yes |
| Page specifications | domain-modeler (04) or user | Natural language / YAML | Yes |
| Theme/branding | User or project config | Colors, fonts | Optional |
| Dashboard design guide | Self (`dashboard_design_guide.md`) | Markdown | Recommended |

## Outputs

| Output | Consumer | Format |
|--------|----------|--------|
| Report ID | `resource_ids.md`, ai-skills (11) | GUID |
| Report definition | Fabric REST API | Legacy PBIX (report.json + definition.pbir + definition.pbism) |
| Deploy script | Project repo | `deploy_report.py` |
| Visual screenshots | project-presentation (02) | Portal render |

## Constraints

1. **MUST use Legacy PBIX format** — PBIR folder renders BLANK (cardinal rule)
2. **`prototypeQuery` MANDATORY** on every data visual — no error message, just blank visual
3. **`definition.pbism`** = `{"version": "1.0"}` ONLY — no connections property
4. **`layoutOptimization: 0`** (integer) required in report.json
5. **All create/update = async** — HTTP 202, poll operation ID (shared constraint #1)
6. **Read-before-write** — GET existing definition before updating (shared constraint #3)
7. **One owner** — no other agent writes to report files (shared constraint #4)
8. **Config-driven** — workspace/model IDs from config, never hardcoded (shared constraint #1)

## Delegation

| When this happens | Delegate to |
|-------------------|-------------|
| Need a semantic model first | semantic-model-agent (09) |
| Need DAX measures added/fixed | semantic-model-agent (09) |
| Need Delta tables / SQL Endpoint | lakehouse-agent (05) |
| Need workspace created | workspace-admin-agent (03) |
| Need Data Agent on top of report | ai-skills-agent (11) |
| Need KQL Dashboard (not PBI) | rti-kusto-agent (14) |

## Error Handling

| Error Pattern | Action |
|---------------|--------|
| HTTP 202 (LRO) | Poll `/operations/{id}` until succeeded/failed |
| HTTP 404 on report | Report deleted — recreate from scratch |
| HTTP 409 conflict | Another operation in progress — wait and retry |
| HTTP 429 throttled | Exponential backoff (2s, 4s, 8s) |
| Blank report in portal | Check: (1) PBIR vs Legacy format (2) missing prototypeQuery (3) wrong model binding |
| Visual shows no data | Check: (1) prototypeQuery syntax (2) model column/measure names (case-sensitive) (3) relationship direction |
| `definition.pbism` error | Must be `{"version": "1.0"}` — no other properties |

## File Inventory

| File | Lines | Purpose |
|------|-------|---------|
| `instructions.md` | System prompt | LOAD FIRST — behavioral rules, decision trees |
| `report_structure.md` | Deep reference | Legacy PBIX anatomy, report.json structure |
| `visual_catalog.md` | Deep reference | All visual types, projections, prototypeQuery |
| `pages_layout.md` | Deep reference | Canvas, grid, page config, dashboard templates |
| `themes_styling.md` | Deep reference | Expression language, colors, fonts, containers |
| `dashboard_design_guide.md` | Design guide | Layout principles, typography, color system |
| `performance.md` | Optimization | Report performance patterns |
| `known_issues.md` | Debugging | Gotchas, workarounds, checklist |
| `templates/` | Scaffolding | Ready-to-use report template + deploy script |

## Validation

After execution, verify:
- [ ] Report exists in workspace (`GET /reports/{id}` returns 200)
- [ ] Report opens in portal without blank pages
- [ ] All visuals show data (not blank)
- [ ] Report binds to correct semantic model
- [ ] Report ID stored in `resource_ids.md` or `state.json`
- [ ] Theme/colors match design specifications
