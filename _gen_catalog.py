import os

base = r'c:\Users\cdroinat\OneDrive - Microsoft\1 - Microsoft\01 - Architecture\-- 004 - Demo\02 - Fabric Démo\Github_Brain\agents\architecture-design-agent\icons'
lines = ['# Icon Catalog — 303 Microsoft Fabric & Azure Icons', '', '> Source: [astrzala/FabricToolset](https://github.com/astrzala/FabricToolset)', '', '---', '']

for cat in sorted(os.listdir(base)):
    cat_path = os.path.join(base, cat)
    if not os.path.isdir(cat_path):
        continue
    svgs = sorted([f for f in os.listdir(cat_path) if f.endswith('.svg')])
    cat_display = cat.replace('_', ' ')
    lines.append(f'## {cat_display} ({len(svgs)} icons)')
    lines.append('')
    lines.append('| Icon Name | File Path |')
    lines.append('|-----------|-----------|')
    for svg in svgs:
        name = svg.replace('.svg', '')
        lines.append(f'| {name} | `icons/{cat}/{svg}` |')
    lines.append('')

out = os.path.join(base, '..', 'icon_catalog.md')
with open(out, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print(f'Written {len(lines)} lines to icon_catalog.md')
