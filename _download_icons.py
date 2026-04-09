"""Download all SVG icons from astrzala/FabricToolset into Github_Brain icons folder."""
import urllib.request
import json
import os
import time

REPO_API = "https://api.github.com/repos/astrzala/FabricToolset/git/trees/main?recursive=1"
RAW_BASE = "https://raw.githubusercontent.com/astrzala/FabricToolset/main/"
DEST_BASE = r"c:\Users\cdroinat\OneDrive - Microsoft\1 - Microsoft\01 - Architecture\-- 004 - Demo\02 - Fabric Démo\Github_Brain\agents\architecture-design-agent\icons"

PREFIX = "Microsoft Fabric & Azure Icon Pack/svg/"

def main():
    # Get repo tree
    req = urllib.request.Request(REPO_API, headers={"User-Agent": "Mozilla/5.0"})
    data = json.loads(urllib.request.urlopen(req).read())
    
    svg_files = [t["path"] for t in data["tree"]
                 if t["path"].startswith(PREFIX) and t["path"].endswith(".svg")]
    
    print(f"Found {len(svg_files)} SVG files to download")
    
    downloaded = 0
    errors = []
    
    for path in svg_files:
        # Extract category and filename
        rel = path[len(PREFIX):]  # e.g. "Azure Core/API Connection.svg"
        parts = rel.split("/")
        if len(parts) == 2:
            category, filename = parts
        else:
            category = "Other"
            filename = parts[-1]
        
        # Normalize category folder name
        cat_folder = category.replace(" ", "_")
        dest_dir = os.path.join(DEST_BASE, cat_folder)
        os.makedirs(dest_dir, exist_ok=True)
        
        # Normalize filename (keep spaces in filename but ensure valid)
        dest_file = os.path.join(dest_dir, filename)
        
        if os.path.exists(dest_file):
            downloaded += 1
            continue
        
        # Build raw URL (URL-encode spaces in path)
        raw_url = RAW_BASE + urllib.request.quote(path, safe="/")
        
        try:
            req = urllib.request.Request(raw_url, headers={"User-Agent": "Mozilla/5.0"})
            svg_data = urllib.request.urlopen(req).read()
            with open(dest_file, "wb") as f:
                f.write(svg_data)
            downloaded += 1
            if downloaded % 25 == 0:
                print(f"  Downloaded {downloaded}/{len(svg_files)}...")
        except Exception as e:
            errors.append((path, str(e)))
            print(f"  ERROR: {filename} - {e}")
        
        # Small delay to avoid rate limiting
        if downloaded % 50 == 0:
            time.sleep(1)
    
    print(f"\nDone! Downloaded {downloaded}/{len(svg_files)} SVG files")
    if errors:
        print(f"Errors ({len(errors)}):")
        for p, e in errors:
            print(f"  {p}: {e}")
    
    # Print summary by category
    print("\nBy category:")
    for cat in sorted(os.listdir(DEST_BASE)):
        cat_path = os.path.join(DEST_BASE, cat)
        if os.path.isdir(cat_path):
            count = len([f for f in os.listdir(cat_path) if f.endswith(".svg")])
            print(f"  {cat}: {count} icons")

if __name__ == "__main__":
    main()
