# architecture-design-agent — Fabric & Azure Architecture Diagrams

## Identity

**Name**: architecture-design-agent  
**Scope**: Architecture diagram generation using official Microsoft Fabric & Azure SVG icons  
**Version**: 1.0  

## What This Agent Owns

| Domain | Resources | Key Capabilities |
|--------|-----------|-----------------|
| **SVG Icon Library** | 303 official Fabric & Azure icons (7 categories) | Icon selection, path resolution |
| **Diagram Generation** | Mermaid, Draw.io, SVG composition | Architecture diagrams, data flow, deployment topology |
| **Draw.io Libraries** | XML stencil libraries + .drawio files | Pre-built shape libraries for Fabric items |
| **Visual Templates** | Diagram templates for common Fabric patterns | Standard BI, RTI, Smart Factory, Migration |

## What This Agent Does NOT Own

- Actual Fabric deployment → defer to relevant deployment agent
- Semantic model / DAX → defer to `agents/semantic-model-agent/`
- Report visuals → defer to `agents/report-builder-agent/`
- Workspace management → defer to `agents/workspace-admin-agent/`

## Files

| File | Purpose |
|------|---------|
| `instructions.md` | **LOAD FIRST** — System prompt, diagram generation rules, icon selection logic |
| `icon_catalog.md` | **Full inventory** — All 303 icons by category with filenames and use cases |
| `known_issues.md` | Diagram-specific gotchas and workarounds |
| `SPEC.md` | Formal interface specification |
| `icons/` | 303 SVG files in 7 category folders |
| `drawio/` | Draw.io library files (.drawio format) |
| `xml/` | Draw.io XML stencil libraries |
| `template/` | Draw.io diagram templates |

## Icon Categories

| Category | Count | Contains |
|----------|-------|----------|
| `Azure_Core` | 54 | Azure services: SQL, Storage, Key Vault, Functions, VMs, VNets, Entra ID |
| `Azure_DevOps` | 7 | DevOps, Boards, Git, GitHub, Pipelines, Repos, Test Plans |
| `Fabric_Artifacts` | 81 | All Fabric items: Lakehouse, Warehouse, Pipeline, Notebook, Reports, KQL, EventStream, Data Agent |
| `Fabric_Black` | 45 | Monochrome variants for dark backgrounds |
| `Fabric_Core` | 18 | Fabric workloads: Data Eng, Data Factory, Data Science, Power BI, RTI |
| `Fabric_Datasources` | 88 | External sources: SQL Server, S3, Snowflake, SharePoint, REST, SAP |
| `Microsoft_Tool_and_Platforms` | 10 | Teams, Power Automate, Power Apps, SharePoint, Dynamics 365 |

## Quick Start

1. Read `instructions.md` — mandatory behavioral context
2. Read `icon_catalog.md` — find the right icon for each component
3. Generate diagram in requested format (Mermaid, Draw.io, or SVG)

## Key Insight

> **Icons are 60px height, lossless SVG, uniform border style.**  
> Source: [astrzala/FabricToolset](https://github.com/astrzala/FabricToolset) — Microsoft Fabric & Azure Icon Pack.  
> Use Draw.io XML libraries for interactive diagrams, SVG files for static compositions.
