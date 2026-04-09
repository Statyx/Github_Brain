# architecture-design-agent — Technical Specification

> Version: 1.0

## Identity

- **Agent**: architecture-design-agent (#22)
- **Category**: Meta / Visualization
- **Owner**: Sole owner of all files in `agents/architecture-design-agent/`

## Inputs

| Input | Source | Format | Required |
|-------|--------|--------|----------|
| Project config | orchestrator (01) or user | YAML / natural language | Yes |
| Diagram scope | User request | Text (e.g., "draw the RTI architecture") | Yes |
| Resource IDs | `resource_ids.md` | GUIDs (for labeling deployed items) | Optional |
| Agent workflow | `WORKFLOWS.md` | Markdown (for agent interaction diagrams) | Optional |
| Icon catalog | Self (`icon_catalog.md`) | Markdown table | Always loaded |

## Outputs

| Output | Consumer | Format |
|--------|----------|--------|
| Mermaid diagram | README, docs, chat | Markdown code block |
| Draw.io XML | User (for editing) | `.drawio` file |
| SVG composition | Docs, presentations | HTML with embedded SVGs |
| Architecture description | project-presentation (02) | Markdown section |

## Constraints

1. **Use official icons only** — Never use generic shapes when an official Fabric/Azure icon exists
2. **Verify icon paths** — Always check `icon_catalog.md` before referencing any icon
3. **Credit source** — Include attribution to astrzala/FabricToolset
4. **60px standard height** — Maintain consistent icon sizing across diagrams
5. **Read-only on other agents** — This agent reads but never modifies other agent files

## Delegation

| When this happens | Delegate to |
|-------------------|-------------|
| Need to understand Fabric item relationships | Read relevant agent's README/instructions |
| Need actual deployment | Delegate to the item-specific agent |
| Need workflow sequence details | Read `WORKFLOWS.md` |
| Need API details for labeling | Read `fabric_api.md` |

## Error Handling

| Error Pattern | Action |
|---------------|--------|
| Icon not found for item type | Use `Fabric_Artifacts/Generic.svg` and note the gap |
| Draw.io library won't load | Provide direct clibs URL from FabricToolset README |
| Mermaid rendering breaks | Simplify subgraph nesting, shorten labels |
| Icon filename has typo | Use as-is (known: `Real-Time Dashoard.svg` — upstream typo) |

## Validation

After execution, verify:
- [ ] All referenced icons exist in `icons/` folder
- [ ] Diagram renders correctly in target format
- [ ] Data flow direction is clear (arrows labeled)
- [ ] All Fabric items use correct official icon
- [ ] Diagram matches the actual project architecture
