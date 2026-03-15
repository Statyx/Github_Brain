# Resource IDs & Endpoints

All Azure and Fabric resource identifiers for the MF_Finance demo.

---

## Azure

| Property | Value |
|----------|-------|
| Subscription | `9b51a6b4-ec1a-4101-a3af-266c89e87a52` |
| Tenant | `92701a21-ddea-4028-ba85-4c1f91fab881` |
| Resource Group | `rg-fabric-demo` |

### Fabric Capacity

| Property | Value |
|----------|-------|
| Name | `cdrfabricdemo` |
| ID | `496a7e48-be58-4da8-9736-4db07711b37c` |
| SKU | F16 |
| Region | westus3 |
| ARM Path | `/subscriptions/9b51a6b4-.../resourceGroups/rg-fabric-demo/providers/Microsoft.Fabric/capacities/cdrfabricdemo` |

---

## Fabric Workspace

| Property | Value |
|----------|-------|
| Name | `CDR - Demo Finance Fabric` |
| ID | `133c6c70-2e26-4d97-aac1-8ed423dbbf34` |

---

## Fabric Items

### Lakehouse
| Property | Value |
|----------|-------|
| Name | `LH_Finance` |
| ID | `f2c42d3b-d402-43e7-b8fb-a9aa395c14e1` |
| SQL Endpoint | `eenhbexk3uueboufjqpzd6vyqe-obwdyezgf2lu3kwbr3kchw57gq.datawarehouse.fabric.microsoft.com` |
| OneLake Path | `https://onelake.dfs.fabric.microsoft.com/133c6c70-2e26-4d97-aac1-8ed423dbbf34/f2c42d3b-d402-43e7-b8fb-a9aa395c14e1/Files/` |

### Notebook
| Property | Value |
|----------|-------|
| Name | `NB_Load_CSV_to_Delta` |
| ID | `86729c39-33a4-454a-8170-0ac363ee809c` |

### Pipeline
| Property | Value |
|----------|-------|
| Name | `PL_Load_Finance_Data` |
| ID | `7fdd5622-9313-4a5f-a769-dccef65a5015` |

### Semantic Model
| Property | Value |
|----------|-------|
| Name | `SM_Finance` |
| ID | `236080b8-3bea-4c14-86df-d1f9a14ac7a8` |
| Mode | Direct Lake |
| Tables | 11 |
| Relationships | 11 |
| DAX Measures | 26 |

### Report (Working)
| Property | Value |
|----------|-------|
| Name | `RPT_Finance_Dashboard` |
| ID | `5b03a794-1088-4a4d-b7f1-ec1a49c6a8ca` |
| Format | Legacy PBIX (Copilot style, matching Finance_Report) |
| Pages | 5 (Financial Performance Overview, P&L Analysis, Budget vs Actuals, Cash Flow & Receivables, Product Profitability) |
| Total Visuals | 49 (across all pages) |
| Generator | `temp/rebuild_report.py` |

### Reference Report (Copilot-created)
| Property | Value |
|----------|-------|
| Name | `Finance_Report` |
| ID | `3381ec85-b4bf-4455-9186-20ccded543e6` |
| Note | Created by Copilot in portal; used as format template |

### Data Agent
| Property | Value |
|----------|-------|
| Name | `Finance_Controller` |
| ID | `01668d9d-0963-46cd-85ac-ee344daf714b` |
| Type | DataAgent |
| Instructions | `docs/data_agent_instructions.md` (5,748 chars, French) |
| Data Source | SM_Finance (must be added in portal) |
| Deployment Script | `src/create_data_agent.py` |
| Tests | `docs/data_agent_examples.md` (25 questions) |

---

## RTI Demo Workspace

| Property | Value |
|----------|-------|
| Name | `CDR - Fabric RTI Demo` |
| ID | _TBD — run deploy_workspace.py to populate_ |
| GitHub | `https://github.com/Statyx/Fabric_RTI_Demo` |

### RTI Demo Items (populated after deployment)
| Item | Type | ID |
|------|------|----|
| EH_SensorTelemetry | Eventhouse | _TBD_ |
| LH_SensorReference | Lakehouse | _TBD_ |
| ES_SensorIngestion | EventStream | _TBD_ |

> IDs are saved in `Fabric RTI Demo/src/state.json` after each deployment step.

---

## API Endpoints

| Service | Base URL | Token Scope |
|---------|----------|-------------|
| Fabric REST API | `https://api.fabric.microsoft.com/v1` | `https://api.fabric.microsoft.com` |
| OneLake DFS | `https://onelake.dfs.fabric.microsoft.com` | `https://storage.azure.com` |
| Azure Resource Manager | `https://management.azure.com` | `https://management.azure.com` |
| SQL Analytics Endpoint | `eenhbexk3...datawarehouse.fabric.microsoft.com` | — |

### Common API Paths
```
GET    /v1/workspaces/{ws_id}/items
POST   /v1/workspaces/{ws_id}/items                          # Create item
POST   /v1/workspaces/{ws_id}/items/{id}/updateDefinition    # Update definition
POST   /v1/workspaces/{ws_id}/items/{id}/getDefinition       # Get definition (parts)
DELETE /v1/workspaces/{ws_id}/items/{id}
GET    /v1/operations/{op_id}                                 # Poll async operation
POST   /v1/workspaces/{ws_id}/items/{id}/jobs/instances?jobType=Pipeline  # Run pipeline
```

### XMLA Connection String (for definition.pbir)
```
Data Source="powerbi://api.powerbi.com/v1.0/myorg/CDR - Demo Finance Fabric";initial catalog=SM_Finance;integrated security=ClaimsToken;semanticmodelid=236080b8-3bea-4c14-86df-d1f9a14ac7a8
```
