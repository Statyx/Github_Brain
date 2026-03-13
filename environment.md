# Environment Setup

## Python 3.12

Installed per-user at:
```
C:\Users\cdroinat\AppData\Local\Programs\Python\Python312\python.exe
C:\Users\cdroinat\AppData\Local\Programs\Python\Python312\Scripts\
```

### PATH Fix (REQUIRED at start of every terminal session)
```powershell
$env:PATH = "C:\Users\cdroinat\AppData\Local\Programs\Python\Python312;C:\Users\cdroinat\AppData\Local\Programs\Python\Python312\Scripts;$env:PATH"
```

### Required Packages
```
pip install requests pyyaml faker azure-cli
```

From `requirements.txt`:
- `requests` — HTTP calls to Fabric/OneLake APIs
- `pyyaml` — Config file parsing
- `faker` — Synthetic data generation
- `azure-cli` — `az account get-access-token` for auth

## Azure CLI

Installed via pip (not MSI):
```powershell
pip install azure-cli
```

Version: 2.84.0+

### Login
```powershell
az login
az account set --subscription "9b51a6b4-ec1a-4101-a3af-266c89e87a52"
```

### Token Commands
```powershell
# Fabric REST API
az account get-access-token --resource "https://api.fabric.microsoft.com" --query accessToken -o tsv

# OneLake / Storage
az account get-access-token --resource "https://storage.azure.com" --query accessToken -o tsv

# Azure Resource Manager
az account get-access-token --resource "https://management.azure.com" --query accessToken -o tsv
```

## PowerShell Gotchas

### BOM-Free File Writing
PowerShell `Out-File` and `Set-Content` add UTF-8 BOM by default. Python's `json.load()` chokes on BOM.

**Fix**: Always use .NET API for JSON files:
```powershell
[System.IO.File]::WriteAllText($path, $content, [System.Text.UTF8Encoding]::new($false))
```

### French Locale
Terminal shows French prompts (`Terminer le programme de commandes (O/N) ?` on Ctrl+C).
Type `O` + Enter to confirm.

### subprocess and `az` Commands
`az` is a `.cmd` wrapper installed via pip. Python `subprocess.run("az rest ...")` hangs.

**Workaround**: Always fetch token separately, then use `requests`:
```python
import subprocess, requests

token = subprocess.check_output(
    ["az", "account", "get-access-token", "--resource", "https://api.fabric.microsoft.com",
     "--query", "accessToken", "-o", "tsv"],
    shell=True
).decode().strip()

headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
resp = requests.get(f"{API}/workspaces", headers=headers)
```

## VS Code Settings

- Terminal: PowerShell 5.1
- Python interpreter: `C:\Users\cdroinat\AppData\Local\Programs\Python\Python312\python.exe`
- Workspace: `c:\Users\cdroinat\OneDrive - Microsoft\1 - Microsoft\01 - Architecture\-- 004 - Demo\02 - Fabric Démo\MF_Finance`

## Azure Automation (Capacity Scheduling)

Runbooks in `src/runbooks/`:
- `Start-FabricCapacity.ps1` → Schedule: Mon-Fri 8:00 AM CET
- `Stop-FabricCapacity.ps1` → Schedule: Mon-Fri 8:00 PM CET

Uses Azure RM API to resume/suspend the F16 Fabric capacity.
