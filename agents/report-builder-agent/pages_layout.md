# Pages & Layout — Canvas Grid System

> **See also**: `dashboard_design_guide.md` for comprehensive design principles, typography scale, color system, and setup checklist.

---

## Design Principles (Quick Reference)

1. **F-Pattern reading**: KPIs top-left → charts middle → detail tables bottom
2. **One story per page**: Each page answers ONE business question
3. **Consistent grid**: All visuals align to the column system below — no arbitrary positioning
4. **White space matters**: Minimum 10px gap between visuals; don't fill every pixel
5. **5-second rule**: User understands the main message within 5 seconds

---

## Standard Canvas

| Property | Value | Notes |
|----------|-------|-------|
| Width | 1280 px | 16:9 aspect ratio |
| Height | 720 px | Standard HD |
| `displayOption` | `1` | Fit to page |

All visual coordinates are relative to this 1280×720 grid.

---

## Margin & Spacing Rules

| Rule | Value |
|------|-------|
| Left/right margin | 30 px |
| Top margin | 10 px |
| Gap between columns | 20 px |
| Gap between rows | 10–15 px |
| Usable width | 1220 px (1280 − 30 − 30) |

---

## Column Systems

### 3-Column Layout (KPI Cards)
```
Usable: 1220 px
Columns: 3
Gap: 20 px
Column width: (1220 - 2×20) / 3 = 390 px (rounded)

x positions:  30  |  440  |  850
```

### 5-Column Compact Layout (KPI Cards — Competitive Marketing Style)
```
Usable: 1220 px
Columns: 5
Gap: 15 px
Column width: (1220 - 4×15) / 5 ≈ 232 px
Card height: 78 px

x positions:  30  |  277  |  524  |  771  |  1018
y position:   69 (just below page title)
```
Best for: **dashboard-dense** overview pages with 5+ KPIs.
Cards use `calloutValue.fontSize` ≤ 21D and title `fontSize` 10–11D for compact fit.

### 2-Column Layout (Charts)
```
Usable: 1220 px
Columns: 2
Gap: 30 px
Column width: (1220 - 30) / 2 = 595 px

x positions:  30  |  655
```

### Full-Width Layout
```
x: 30, width: 1220
```

---

## Recommended Heights

| Element | Height | Notes |
|---------|--------|-------|
| Title bar (textbox) | 40 px | Dashboard heading |
| KPI Card | 120 px | Minimum for readable calloutValue |
| Small Chart | 185 px | |
| Medium Chart | 250 px | More detail / labels |
| Large Chart | 350 px | Complex charts, tables |
| Slicer | 40–60 px | Dropdown style |
| Table / Matrix | 200–350 px | Depends on row count |

**CRITICAL**: Card height must be ≥ 120px when `calloutValue.fontSize: 27D`, otherwise values clip.

---

## Dashboard Templates

### Template A: Executive Overview (6 KPIs + 4 Charts)

```
y=10    [─────────── Title Bar (1220×40) ───────────]

y=60    [ KPI 1 (390×120) ] [ KPI 2 (390×120) ] [ KPI 3 (390×120) ]

y=190   [ KPI 4 (390×120) ] [ KPI 5 (390×120) ] [ KPI 6 (390×120) ]

y=325   [ Chart 1 (595×185) ]    [ Chart 2 (595×185) ]

y=525   [ Chart 3 (595×185) ]    [ Chart 4 (595×185) ]

Total: 710 px → fits in 720 canvas
```

Visual coordinates:
| Visual | x | y | width | height |
|--------|---|---|-------|--------|
| Title | 30 | 10 | 1220 | 40 |
| KPI 1 | 30 | 60 | 390 | 120 |
| KPI 2 | 440 | 60 | 390 | 120 |
| KPI 3 | 850 | 60 | 390 | 120 |
| KPI 4 | 30 | 190 | 390 | 120 |
| KPI 5 | 440 | 190 | 390 | 120 |
| KPI 6 | 850 | 190 | 390 | 120 |
| Chart 1 | 30 | 325 | 595 | 185 |
| Chart 2 | 655 | 325 | 595 | 185 |
| Chart 3 | 30 | 525 | 595 | 185 |
| Chart 4 | 655 | 525 | 595 | 185 |

### Template B: KPI Row + One Large Chart

```
y=10    [─────────── Title Bar (1220×40) ───────────]

y=60    [ KPI 1 (390×120) ] [ KPI 2 (390×120) ] [ KPI 3 (390×120) ]

y=195   [──────────── Large Chart (1220×350) ────────────]

y=560   [──────── Slicer Row (1220×50) ────────]
```

### Template C: Table/Matrix Focus

```
y=10    [─────────── Title Bar (1220×40) ───────────]

y=60    [ KPI 1 (295×120) ] [ KPI 2 (295×120) ] [ KPI 3 (295×120) ] [ KPI 4 (295×120) ]

y=195   [──────────── Table or Matrix (1220×510) ────────────]
```

4-column for KPI row:
```
Column width: (1220 - 3×20) / 4 = 290 px (rounded to 295)
x positions:  30  |  335  |  640  |  945
Widths: 295 each (last one: 285 to fit)
```

---

## Multi-Page Reports

### Adding Pages

Each page is a `section` in the `sections[]` array:

```python
sections = [
    make_section("Overview", "Executive Overview", overview_visuals),
    make_section("Revenue", "Revenue Analysis", revenue_visuals),
    make_section("Budget", "Budget vs Actual", budget_visuals),
    make_section("AR", "Accounts Receivable", ar_visuals),
]
```

### Page Naming Rules
- `name`: Internal identifier — no spaces, no special characters, unique per report
- `displayName`: User-visible tab name — spaces OK, unicode OK
- `config`: Must contain `{"name": "<name>"}` stringified — name must match the `name` field

### Page Order
Pages appear in the order they occur in `sections[]`. First page is shown by default.
The `activeSectionIndex` in report config controls which page opens first (0-based).

---

## Z-Index Stacking

The `z` property controls visual overlap order:
- `z: 0` — Background elements (shapes, images)
- `z: 1` — Standard visuals (cards, charts)
- `z: 2+` — Overlapping elements
- Higher `z` = on top

---

## Python: Layout Helpers

```python
def kpi_row_3col(y: int, measures: list[tuple[str, str, str]], table: str = "fact_general_ledger"):
    """Generate 3 KPI cards in a row.
    
    Args:
        y: Y position of the row
        measures: List of (measure_name, title, visual_id) tuples
    """
    x_positions = [30, 440, 850]
    visuals = []
    for i, (measure, title, vid) in enumerate(measures):
        visuals.append(make_card(vid, x_positions[i], y, 390, 120, table, measure, title))
    return visuals

def chart_row_2col(y: int, chart1_config: dict, chart2_config: dict):
    """Position two chart configs side by side."""
    chart1_config["layouts"][0]["position"].update({"x": 30, "y": y, "width": 595, "height": 185})
    chart2_config["layouts"][0]["position"].update({"x": 655, "y": y, "width": 595, "height": 185})
    return [chart1_config, chart2_config]

def full_width(y: int, height: int, config: dict):
    """Position a visual full-width."""
    config["layouts"][0]["position"].update({"x": 30, "y": y, "width": 1220, "height": height})
    return config
```

---

## Finance Dashboard — RPT_Finance_Dashboard (5 Pages)

Uses the **Copilot standard layout** matching the working `Finance_Report` in the same workspace. Light theme with drop shadows, accent bars on cards.

### Standard Page Layout (Copilot Style)

```
┌────────────────────────────────────────────────────────────────┐
│ Header bar (shape)     h=80          [Slicer1] [Slicer2]      │  y=0
│ Page Title (textbox)   z=2                                     │  y=20
├──────────────────────────────┬─────────────────────────────────┤
│ Card 1  (w=595, h=112)      │ Card 2   (w=595, h=112)        │  y=100
├──────────────────────────────┬─────────────────────────────────┤
│ Chart 1 (w=595, h=224)      │ Chart 2  (w=595, h=224)        │  y=222
├──────────────────────────────┬─────────────────────────────────┤
│ Chart 3 (w=595, h=224)      │ Chart 4  (w=595, h=224)        │  y=456
└──────────────────────────────┴─────────────────────────────────┘
```

Grid: x=40 (left col), x=645 (right col), w=595 each

| Element | x | y | z | w×h | Notes |
|---------|---|---|---|-----|-------|
| Header shape | 0 | 0 | 1 | 1280×80 | fill=off, outline=off, dropShadow=on |
| Page title | 40 | 20 | 2 | 620×40 | Segoe UI 14pt bold |
| Slicer 1 | 840 | 0 | 2 | 212×72 | Dropdown mode |
| Slicer 2 | 1068 | 0 | 2 | 212×72 | Dropdown mode |
| Card left | 40 | 100 | 1 | 595×112 | cardVisual with accentBar |
| Card right | 645 | 100 | 1 | 595×112 | cardVisual with accentBar |
| Chart TL | 40 | 222 | 1 | 595×224 | Any axis chart |
| Chart TR | 645 | 222 | 1 | 595×224 | Any axis chart |
| Chart BL | 40 | 456 | 1 | 595×224 | Any axis chart |
| Chart BR | 645 | 456 | 1 | 595×224 | Any axis chart |

### vcObjects (standard for all visuals)

```json
"vcObjects": {
  "dropShadow": [{"properties": {"show": "true", "color": "#A6ADC6", "preset": "Custom", "shadowSpread": "0L", "shadowBlur": "5L", "angle": "90L", "shadowDistance": "4L", "transparency": "85L"}}],
  "background": [{"properties": {"show": "true"}}],
  "border": [{"properties": {"show": "true", "color": "#E0E0E0", "radius": "4L"}}],
  "title": [{"properties": {"show": "true", "text": "'Chart Title'"}}]
}
```

### Card objects (standard)

```json
"objects": {
  "accentBar": [{"properties": {"color": "#118DFF"}, "selector": {"metadata": "table.Measure"}}],
  "outline": [{"properties": {"show": "false"}}],
  "layout": [{"properties": {"maxTiles": "10L"}}]
}
```

### Slicer objects (standard)

```json
"objects": {
  "data": [{"properties": {"mode": "Dropdown"}}],
  "header": [{"properties": {"show": "true", "fontFamily": "Segoe UI", "textSize": "9L"}}],
  "selection": [{"properties": {"selectAllCheckboxEnabled": "true"}}]
}
```

### Page 1: Financial Performance Overview (10 visuals)
| Slicers | period_month, fiscal_year |
| Cards | Total Revenue, Net Income |
| Charts | Gross Profit by Fiscal Year (bar), EBITDA by Month (line), Gross Margin % by Fiscal Year (bar), Net Income by Month (line) |

### Page 2: P&L Analysis (10 visuals)
| Slicers | period_month, fiscal_year |
| Cards | Total Revenue, Total COGS |
| Charts | Revenue vs COGS by Month (clustered column, 2 measures), Margin Trends (line, 2 measures), Revenue by Sub-Category (bar), OpEx by Cost Center (bar) |

### Page 3: Budget vs Actuals Analysis (10 visuals)
| Slicers | cost_center_name, fiscal_year |
| Cards | Budget Amount, Actual Amount |
| Charts | Budget vs Actual by Account (bar, 2 measures), Variance by Account (bar), Variance % by Month (line), Variance by Cost Center (bar) |

### Page 4: Cash Flow & Receivables (10 visuals)
| Slicers | region, fiscal_year |
| Cards | Total AR, DSO |
| Charts | AR by Customer (bar), Invoices by Status (donut), Overdue by Customer (bar), Paid vs Unpaid by Region (column, 2 measures) |

### Page 5: Product Profitability Analysis (9 visuals)
| Slicers | category (1 slicer only) |
| Cards | Gross Profit, Gross Margin % |
| Charts | Revenue by Product (bar), Revenue vs COGS Trend (line, 2 measures), Gross Profit by Category (bar), Gross Profit Trend (line) |

### Generation Script

The report is generated by `temp/rebuild_report.py` using the exact visual format from the Copilot-generated Finance_Report reference. Deploy with:
```bash
python temp/rebuild_report.py          # Generate report.json
python src/deploy_report.py --from-file report.json  # Deploy to Fabric
```

---

## PBIX-Validated Visual Size Ranges

> Extracted from 7 production Power BI reports (35 pages, 792+ visuals).
> Use these ranges as **guardrails** — the grid templates above remain the primary layout system.

### KPI Cards

| Report Pattern | Width (px) | Height (px) | Width % | Height % | Cards/Row |
|---------------|-----------|------------|---------|----------|----------|
| Corporate Spend | ~192 | ~94 | 15% | 13% | 5–6 |
| Revenue Opportunities | ~218 | ~94 | 17% | 13% | 4–5 |
| **Competitive Marketing** | **232** | **78** | **18%** | **11%** | **5** |
| Regional Sales KPIs | ~300 | ~68 | 23% | 9.5% | 4 |
| **Brain Template** | **390** | **120** | **30%** | **17%** | **3** |

**Takeaway**: Real-world cards are often **smaller** than our 390×120 template. Use the **5-Column Compact** layout (232×78px) for dashboard-dense pages with 5 KPIs — the Competitive Marketing pattern. Use 300×100 for 4-card rows, or 200×90 for 5–6 card dense layouts. Minimum height 68px works when `calloutValue.fontSize` is ≤ 21D.

### Charts

| Visual Type | Width Range (px) | Height Range (px) | Typical Use |
|-------------|-----------------|-------------------|-------------|
| Bar Chart | 256–1242 (20–97%) | 200–360 (28–50%) | Category comparison |
| Line Chart | 614–870 (48–68%) | 200–360 (28–50%) | Trend analysis |
| Combo Chart | 294–883 (23–69%) | 223–432 (31–60%) | Dual-axis analysis |
| Donut/Pie | 300–500 (23–39%) | 250–360 (35–50%) | Proportion |

**Takeaway**: Charts rarely go below 200px height. Full-width charts (>900px) are used for single focal points. Half-width (~600px) is standard for 2-column grid.

### Tables & Matrices

| Metric | Range (px) | Range (%) |
|--------|-----------|----------|
| Width | 806–1216 | 63–95% |
| Height | 346–641 | 48–89% |

**Takeaway**: Tables are almost always wide (>60% canvas). They dominate the lower half of a page. Never place a table in a narrow column.

### Slicers

| Metric | Range (px) | Range (%) | Position |
|--------|-----------|----------|----------|
| Width | 205–371 | 16–29% | Top-right |
| Height | 50–72 | 7–10% | Aligned with title row |

**Takeaway**: Slicers are compact — a single row of dropdowns, aligned top-right. They never take more than 30% width.

---

## Tooltip Page Configuration

Tooltip pages use custom dimensions (not the standard 1280×720).

| Tooltip Style | Width | Height | Use Case |
|--------------|-------|--------|----------|
| Standard | 320 | 240 | Simple KPI tooltip |
| Tall | 300 | 370 | Multi-metric tooltip |
| Square | 325 | 325 | Chart + KPI combo |
| Compact | 311 | 285 | 2–3 values |
| Wide | 698 | 360 | Detail table tooltip |

### Tooltip Page Config
```python
def make_tooltip_section(name, display_name, width, height, visuals):
    config = json.dumps({
        "name": name,
        "layouts": [{"id": 0, "position": {"x": 0, "y": 0, "z": 0, "width": width, "height": height}}],
        "visibility": 1,  # Hidden from page tabs
        "displayOption": 1,
        "defaultSize": {"type": 6},  # Custom size
        "objectId": secrets.token_hex(16),
    })
    return {
        "name": name,
        "displayName": display_name,
        "width": width,
        "height": height,
        "config": config,
        "visualContainers": visuals,
    }
```

---

## Template D: Navigation Sidebar (Multi-Page Reports)

> **Source**: Regional Sales Sample (11 pages, 732 action buttons)

For reports with 5+ pages, use a left sidebar with `actionButton` visuals for page navigation.

```
┌──────┬──────────────────────────────────────────────┐
│ Nav  │ [Title]                          y=10, h=40  │
│ Bar  ├──────────┬──────────┬──────────┬─────────────┤
│      │ KPI 1    │ KPI 2    │ KPI 3    │   y=60      │
│ 80px ├──────────┴──────────┴──────────┤             │
│ wide │ [Main Content Area]             │   y=190     │
│      │ 1120px wide (1280−80−30−30−20)  │             │
│      │                                 │             │
│      │                                 │             │
└──────┴─────────────────────────────────┘
```

| Element | x | y | width | height |
|---------|---|---|-------|--------|
| Nav sidebar (basicShape) | 0 | 0 | 80 | 720 |
| Nav button 1 | 10 | 60 | 60 | 50 |
| Nav button 2 | 10 | 120 | 60 | 50 |
| Nav button N | 10 | 60+N×60 | 60 | 50 |
| Content area x-start | 100 | — | — | — |
| Usable content width | — | — | 1150 | — |

**Navigation buttons** use `actionButton` visual type with `action.type = "PageNavigation"` and `action.pageLink` pointing to the target section name.

---

## Template E: Full HD Canvas (1920×1080)

> **Source**: Store Sales (5 pages at 1920×1080)

| Property | Value | Notes |
|----------|-------|-------|
| Width | 1920 px | 16:9 Full HD |
| Height | 1080 px | More vertical space |
| `displayOption` | `1` | Fit to page |
| Margins (L/R) | 40 px | Slightly wider |
| Usable width | 1840 px | 1920 − 40 − 40 |

### When to use Full HD:
- Large-screen displays / conference rooms
- Data-dense dashboards with 10+ visuals per page
- Reports embedded in portals at fixed size

### Full HD 3-Column Grid
```
Usable: 1840 px
Columns: 3
Gap: 30 px
Column width: (1840 - 2×30) / 3 = 593 px

x positions:  40  |  663  |  1286
```

---

## Decorative & Structural Elements

Real-world reports use non-data visuals extensively for polish:

| Visual Type | Count (7 reports) | Purpose |
|-------------|-------------------|----------|
| `actionButton` | 792 | Page navigation, drill-through links |
| `basicShape` | 86 | Background panels, section separators, colored bars |
| `shape` | 68 | Decorative borders, accent lines |
| `textbox` | 63 | Titles, section headers, annotations |
| `visualGroup` | 47 | Grouped visuals for layered page templates |
| `image` | 18 | Logos, brand icons |

### Colored Header Bar Pattern
```python
# A thin colored bar across the top of the page
header_bar = {
    "name": "header_accent",
    "layouts": [{"id": 0, "position": {"x": 0, "y": 0, "z": 0, "width": 1280, "height": 5}}],
    "singleVisual": {
        "visualType": "basicShape",
        "objects": {
            "line": [{"properties": {"show": _lit("false")}}],
            "fill": [{"properties": {"fillColor": _color("#118DFF"), "transparency": _lit("0L")}}],
        },
    },
}
```

### Section Separator Pattern
```python
# Horizontal line between visual sections
separator = {
    "name": "section_sep",
    "layouts": [{"id": 0, "position": {"x": 30, "y": 315, "z": 0, "width": 1220, "height": 2}}],
    "singleVisual": {
        "visualType": "basicShape",
        "objects": {
            "line": [{"properties": {"show": _lit("false")}}],
            "fill": [{"properties": {"fillColor": _color("#E0E0E0"), "transparency": _lit("0L")}}],
        },
    },
}
```
