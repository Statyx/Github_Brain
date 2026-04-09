# architecture-design-agent — Known Issues

## Draw.io

| Issue | Workaround |
|-------|-----------|
| XML library doesn't load in draw.io online | Use the direct clibs URL from the FabricToolset README. Clear browser cache if stale. |
| Custom shapes show as blank | Re-import the XML library. Some versions of draw.io cache old shapes. |
| SVG icons appear oversized | Set explicit width/height. All icons are designed for 60px height. |

## Mermaid

| Issue | Workaround |
|-------|-----------|
| Mermaid doesn't support SVG icons natively | Use descriptive node labels + shapes. Reference icon catalog for correct naming. |
| Long node labels break layout | Use abbreviations in diagram, add legend below. |
| Subgraph nesting limited to 2 levels | Flatten to 2 levels max. Use color coding instead of deep nesting. |

## SVG Composition

| Issue | Workaround |
|-------|-----------|
| Filenames with spaces break in some tools | URL-encode spaces: `Semantic%20Model.svg` |
| Some icons have inconsistent padding | The icon pack should be uniform 60px, but verify if visual looks off. |
| `Real-Time Dashoard.svg` is misspelled | Known upstream typo. Use as-is — it's the correct file for KQL Dashboards. |

## General

| Issue | Workaround |
|-------|-----------|
| Missing icon for a new Fabric item | Check for updates at [astrzala/FabricToolset](https://github.com/astrzala/FabricToolset). Use `Fabric_Artifacts/Generic.svg` as placeholder. |
| Need dark-mode variant | Use `Fabric_Black/` category (45 monochrome icons). Not all items have black variants. |
