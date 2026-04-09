# Themes & Styling — Expression Language, Colors, Typography, Python Helpers

> **See also**: `dashboard_design_guide.md` for complete design system, layout templates, and setup checklist.

---

## Typography Quick Reference

Use **ONE font family** (Segoe UI) and differentiate via size and weight only.

| Role | Size | Weight | JSON Value |
|------|------|--------|------------|
| Page title | 14pt | Bold | `"14D"` |
| Visual title | 11pt | Regular | `"11D"` |
| KPI callout | 27pt | Semibold | `"27D"` — **never leave default** |
| Axis / Legend / Labels | 10pt | Regular | `"10D"` |
| Data labels | 9pt | Regular | `"9D"` |
| Table header | 11pt | Semibold | `"11D"` |
| Table body | 10pt | Regular | `"10D"` |

**Minimum readable size**: 9pt. Never go below this.

---

## PBI Expression Language

Power BI config JSON uses a verbose expression language for property values.
These patterns appear hundreds of times — helper functions are essential.

### Literal Values

```json
{"expr": {"Literal": {"Value": "true"}}}         // boolean true
{"expr": {"Literal": {"Value": "false"}}}        // boolean false
{"expr": {"Literal": {"Value": "27D"}}}          // number (D suffix = double/decimal)
{"expr": {"Literal": {"Value": "0L"}}}           // integer (L suffix = long)
{"expr": {"Literal": {"Value": "'#FF0000'"}}}    // string (single-quoted inside JSON string)
{"expr": {"Literal": {"Value": "'Custom'"}}}     // string enum
```

### Type Suffix Reference

| Suffix | Type | Example | Meaning |
|--------|------|---------|---------|
| `D` | double/decimal | `"27D"` | 27pt font size |
| `L` | long/integer | `"4L"` | 4px distance |
| `'...'` | string | `"'#A6ADC6'"` | Color hex string |
| none | boolean | `"true"` | Boolean value |

### Color Value
```json
{"solid": {"color": {"expr": {"Literal": {"Value": "'#A6ADC6'"}}}}}
```

### Source Reference
```json
{"SourceRef": {"Source": "f"}}   // reference to alias in From clause
```

---

## Python Helper Functions

```python
def _lit(value: str) -> dict:
    """Wrap a raw literal: 'true', '27D', \"'#FF0000'\", etc."""
    return {"expr": {"Literal": {"Value": value}}}

def _color(hex_color: str) -> dict:
    """Solid color property. hex_color includes #, e.g. '#FF0000'."""
    return {"solid": {"color": _lit(f"'{hex_color}'")}}

def _source_ref(alias: str) -> dict:
    return {"SourceRef": {"Source": alias}}

def _measure_expr(alias: str, prop: str) -> dict:
    return {"Measure": {"Expression": _source_ref(alias), "Property": prop}}

def _column_expr(alias: str, prop: str) -> dict:
    return {"Column": {"Expression": _source_ref(alias), "Property": prop}}

def _bool(val: bool) -> dict:
    return _lit("true" if val else "false")

def _int(val: int) -> dict:
    return _lit(f"{val}L")

def _float(val: float) -> dict:
    return _lit(f"{val}D")

def _str(val: str) -> dict:
    return _lit(f"'{val}'")
```

---

## Container Styling (vcObjects)

`vcObjects` = container-level styling. Goes in `singleVisual.vcObjects`.
This controls the visual's frame: title, background, border, shadow.

### Title
```python
"title": [{"properties": {
    "show":      _lit("true"),
    "text":      _lit("'My Visual Title'"),
    "fontSize":  _lit("12D"),           # optional
    "fontColor": _color("#333333"),      # optional
    "bold":      _lit("true"),           # optional
}}]
```

### Drop Shadow
```python
"dropShadow": [{"properties": {
    "show":          _lit("true"),
    "color":         _color("#A6ADC6"),
    "preset":        _lit("'Custom'"),
    "shadowSpread":  _lit("0L"),
    "shadowBlur":    _lit("5L"),
    "angle":         _lit("90L"),
    "shadowDistance": _lit("4L"),
    "transparency":  _lit("85L"),
}}]
```

### Background
```python
"background": [{"properties": {
    "show":         _lit("true"),
    "color":        _color("#FFFFFF"),    # optional - defaults to white
    "transparency": _lit("0L"),           # optional - 0=opaque, 100=transparent
}}]
```

### Border
```python
"border": [{"properties": {
    "show":   _lit("true"),
    "color":  _color("#E0E0E0"),
    "radius": _lit("4L"),          # corner radius in px
    "width":  _lit("1L"),          # optional border width
}}]
```

### Full vcObjects Builder
```python
def make_vc_objects(title_text=None, shadow=True, background=True, border=True):
    vc = {}
    
    if title_text:
        vc["title"] = [{"properties": {
            "show": _lit("true"),
            "text": _lit(f"'{title_text}'"),
        }}]
    
    if shadow:
        vc["dropShadow"] = [{"properties": {
            "show":          _lit("true"),
            "color":         _color("#A6ADC6"),
            "preset":        _lit("'Custom'"),
            "shadowSpread":  _lit("0L"),
            "shadowBlur":    _lit("5L"),
            "angle":         _lit("90L"),
            "shadowDistance": _lit("4L"),
            "transparency":  _lit("85L"),
        }}]
    
    if background:
        vc["background"] = [{"properties": {"show": _lit("true")}}]
    
    if border:
        vc["border"] = [{"properties": {
            "show":   _lit("true"),
            "color":  _color("#E0E0E0"),
            "radius": _lit("4L"),
        }}]
    
    return vc
```

---

## Visual-Specific Objects (objects)

`objects` = visual-type-specific formatting. Goes in `singleVisual.objects`.

### Card (cardVisual)
```python
"objects": {
    "outline":       [{"properties": {"show": _lit("false")}}],
    "calloutValue":  [{"properties": {"fontSize": _lit("27D")}}],
    "categoryLabel": [{"properties": {"show": _lit("false")}}],
}
```

**CRITICAL**: Default `calloutValue` font size is enormous. Always set to `27D` (27pt).
Card height must be ≥ 120px to avoid clipping.

### Chart Axes
```python
"objects": {
    "categoryAxis": [{"properties": {
        "showAxisTitle": _lit("true"),
        "fontSize":      _lit("10D"),     # optional
    }}],
    "valueAxis": [{"properties": {
        "showAxisTitle": _lit("true"),
        "fontSize":      _lit("10D"),     # optional
    }}],
}
```

### Chart Legend
```python
"objects": {
    "legend": [{"properties": {
        "show":     _lit("true"),
        "position": _lit("'Top'"),         # Top, Bottom, Left, Right
        "fontSize": _lit("10D"),
    }}],
}
```

### Chart Data Labels
```python
"objects": {
    "labels": [{"properties": {
        "show":     _lit("true"),
        "fontSize": _lit("10D"),
        "color":    _color("#333333"),
    }}],
}
```

### Textbox (paragraphs)
```python
"objects": {
    "general": [{"properties": {
        "paragraphs": [{
            "textRuns": [{
                "value": "Dashboard Title",
                "textStyle": {
                    "fontFamily": "Segoe UI",
                    "fontSize": "14pt",
                    "fontWeight": "bold",
                }
            }],
            "horizontalTextAlignment": "left"
        }]
    }}]
}
```

---

## Base Theme

The base theme file is required for proper rendering. Current project uses `CY26SU02`.

### In report.json
```json
{
  "theme": "CY26SU02",
  "resourcePackages": [{
    "resourcePackage": {
      "name": "SharedResources",
      "type": 2,
      "items": [{"type": 202, "path": "BaseThemes/CY26SU02.json", "name": "CY26SU02"}],
      "disabled": false
    }
  }]
}
```

### In report config (stringified)
```json
{
  "themeCollection": {
    "baseTheme": {
      "name": "CY26SU02",
      "version": {"visual": "2.6.0", "report": "3.1.0", "page": "2.3.0"},
      "type": 2
    }
  }
}
```

### In API parts
```json
{
  "path": "StaticResources/SharedResources/BaseThemes/CY26SU02.json",
  "payload": "<base64-encoded-theme-json>",
  "payloadType": "InlineBase64"
}
```

### Getting the Theme File
Extract from an existing report via `getDefinition`:
```python
for part in result["definition"]["parts"]:
    if "BaseThemes" in part["path"]:
        theme_b64 = part["payload"]
        theme_json = json.loads(base64.b64decode(theme_b64))
        break
```

---

## Color Palette — Fluent 2 (Active)

The current project palette uses the **Fluent 2** theme — Microsoft's modern default, extracted from 7 production PBIX reports. Blue-focused, high-contrast, and designed for screen readability.

### Data Colors (8-series palette)

| # | Name | Hex | Usage |
|---|------|-----|-------|
| 1 | **Blue** | `#118DFF` | Primary series, positive indicators |
| 2 | **Navy** | `#12239E` | Secondary series, dark contrast |
| 3 | **Orange** | `#E66C37` | Tertiary series, warm accent |
| 4 | **Purple** | `#6B007B` | Deep accent |
| 5 | **Pink** | `#E044A7` | Highlight accent |
| 6 | **Violet** | `#744EC2` | Mid-range accent |
| 7 | **Gold** | `#D9B300` | Warning, neutral series |
| 8 | **Red** | `#D64550` | Negative / alert indicators |

### Semantic Colors

| Purpose | Hex | Notes |
|---------|-----|-------|
| Good / Positive | `#1AAB40` | Green — distinct from primary blue |
| Bad / Negative | `#D64554` | Red — high contrast on white |
| Neutral / Warning | `#D9B300` | Gold — attention without alarm |
| Maximum | `#118DFF` | Gradient max (blue) |
| Minimum | `#DEEFFF` | Very light blue (gradient min) |

### Structural Colors

| Element | Hex | Source |
|---------|-----|--------|
| Text (primary) | `#252423` | Dark charcoal — Fluent 2 standard |
| Text (secondary) | `#616161` | Medium gray for labels, subtitles |
| Borders | `#c7c8ce` | Cool gray — subtle card edges |
| Shadows | `#cccccc` | Soft gray — no colored shadows |
| Accent bar | `#118DFF` | Blue header accent |
| Background panels | `#F6F6F6` | Near-white KPI grouping |
| Page background | `#FFFFFF` | Pure white canvas |
| Dividers / separators | `#cccccc` | Same as shadows |

### Design Rationale (from PBIX analysis)
- **Dark charcoal text** (`#252423`) instead of pure black — softer on the eyes, Fluent 2 standard
- **Cool gray borders** (`#c7c8ce`) — neutral, doesn't compete with data colors
- **No colored drop shadows** — subtle gray from PBIX analysis
- **White background** — clean, professional, lets the blue data colors stand out
- DIN font for visual titles, Segoe UI Semibold for callouts — matches Fluent 2 text classes
- Blue + navy + orange + purple provides excellent contrast and is colorblind-friendly

---

## Table Alias Builder

When a visual references multiple tables, each needs a unique alias:

```python
def build_aliases(tables: list[str]) -> tuple[dict, list]:
    """Build alias map and From clause for prototypeQuery.
    
    Returns:
        alias_map: {"fact_general_ledger": "f", "dim_calendar": "d", ...}
        from_list: [{"Name": "f", "Entity": "fact_general_ledger", "Type": 0}, ...]
    """
    alias_map = {}
    from_list = []
    for t in tables:
        if t not in alias_map:
            alias_map[t] = chr(ord("a") + len(alias_map))
            from_list.append({"Name": alias_map[t], "Entity": t, "Type": 0})
    return alias_map, from_list
```

### Common Aliases in Finance Model
| Table | Alias |
|-------|-------|
| `fact_general_ledger` | `f` or `a` |
| `dim_calendar` | `c` or `b` |
| `dim_cost_centers` | `d` or `c` |
| `dim_accounts` | `e` or `d` |
| `fact_budget` | `g` or `e` |
| `fact_ar_invoices` | `h` or `f` |

---

## Built-in Theme Reference

> Extracted from 7 production PBIX reports. These themes ship with Power BI.

### Fluent 2 (Modern Standard — Recommended)

The current default Power BI theme. Use as baseline for all new reports.

| Property | Value |
|----------|-------|
| `name` | `"Fluent 2"` |
| Data Colors | `#118DFF`, `#12239E`, `#E66C37`, `#6B007B`, `#E044A7`, `#744EC2`, `#D9B300`, `#D64550` |
| Background | `#FFFFFF` |
| Foreground | `#252423` |
| Table Accent | `#118DFF` |
| Good | `#1AAB40` |
| Bad | `#D64554` |
| Neutral | `#D9B300` |
| Maximum | `#118DFF` |
| Minimum | `#DEEFFF` |
| Center | `#C7E5FF` |

#### Fluent 2 Text Classes
| Class | Font | Size | Color |
|-------|------|------|-------|
| `callout` | Segoe UI Semibold | 21pt | `#252423` |
| `title` | DIN | 12pt | `#252423` |
| `header` | Segoe UI Semibold | 12pt | `#252423` |
| `label` | Segoe UI | 10.5pt | `#616161` |

> **Note**: Fluent 2 uses DIN for visual titles and Segoe UI Semibold for callout values (KPI cards). This matches the patterns seen in the production reports.

### Solar (Warm/Energy Theme)

| Property | Value |
|----------|-------|
| Data Colors | `#FFAC00`, `#EE5A00`, `#B44400`, `#8A2400`, `#5C0001`, `#DEBF8C`, `#89620D`, `#FFC961` |
| Background | `#FFFFFF` |
| Foreground | `#000000` |
| Good | `#1AAB40` |
| Bad | `#D64554` |

Best for: Energy dashboards, warm-toned industry reports.

### NewExecutive (Corporate/Blue)

| Property | Value |
|----------|-------|
| Data Colors | `#3257A8`, `#4A97C9`, `#6BC1AF`, `#A6DA72`, `#F4EC3A`, `#ECCD67`, `#E8A55B`, `#DEB6CF` |
| Background | `#FFFFFF` |
| Foreground | `#232323` |
| Good | `#1AAB40` |
| Bad | `#D64554` |

Best for: Executive/boardroom presentations, corporate finance.

---

## Theme-Relative Color Expressions (ThemeDataColor)

Instead of hardcoding hex colors, reference the active theme's data color palette:

```json
{"expr": {"ThemeDataColor": {"ColorId": 0, "Percent": 0}}}
```

| Parameter | Meaning |
|-----------|----------|
| `ColorId` | 0-based index into `dataColors[]` array |
| `Percent` | Lightness adjustment: negative = darker, positive = lighter, 0 = exact |

### Examples
```python
def _theme_color(color_id: int, percent: float = 0) -> dict:
    """Reference a theme data color with optional lightness adjustment."""
    return {"solid": {"color": {"expr": {"ThemeDataColor": {"ColorId": color_id, "Percent": percent}}}}}

# First theme color (primary)
_theme_color(0)       # Fluent 2: #118DFF
# Second color, 20% lighter
_theme_color(1, 0.2)  # Fluent 2: lighter #12239E
# Seventh color (warning)
_theme_color(6)       # Fluent 2: #D9B300
```

### Advantage Over Hardcoded Colors
- Report automatically updates if user changes theme
- Ensures palette consistency across all visuals
- Use `Percent` to create lighter/darker variants without new hex values

---

## Gradient Fills (Conditional Color)

Used for heat maps, KPI conditional coloring, and data bars. Observed heavily in Regional Sales and Corporate Spend reports.

### linearGradient2 Pattern (Two-Stop Gradient)
```python
def _gradient_fill(measure_table: str, measure_name: str, min_color: str, max_color: str, alias: str = "f") -> dict:
    """Create a 2-stop gradient fill bound to a measure."""
    return {
        "FillRule": {
            "linearGradient2": {
                "min": {"color": _lit(f"'{min_color}'")},
                "max": {"color": _lit(f"'{max_color}'")},
            },
            "inputValue": {
                "Measure": {
                    "Expression": {"SourceRef": {"Source": alias}},
                    "Property": measure_name
                }
            }
        }
    }
```

### Usage in Visual Objects
```python
# Heat map on a table column
"objects": {
    "values": [{
        "properties": {
            "backColor": {
                "solid": {"color": {"expr": _gradient_fill("fact", "Sales", "#DEEFFF", "#118DFF")}}
            }
        }
    }]
}
```

### Common Gradient Palettes
| Purpose | Min Color | Max Color | Notes |
|---------|-----------|-----------|-------|
| Blue intensity | `#DEEFFF` | `#118DFF` | Good default, Fluent 2 aligned |
| Red alert | `#FDDEDE` | `#D64554` | Highlight high-risk values |
| Green performance | `#E6F5E6` | `#1AAB40` | Performance metrics |
| Warm (Solar) | `#FFC961` | `#EE5A00` | Energy/heat displays |
