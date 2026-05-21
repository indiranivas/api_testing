# Quick Start

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Start Server

```bash
uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

## 3. Open API Docs

Go to: `http://localhost:8000/docs`

You'll see the Swagger UI with all endpoints.

## 4. Test the API

**Option A: Use Swagger UI**
- Click **POST** `/api/v1/telemetry`
- Click **Try it out**
- Paste this JSON:

```json
{
  "session_id": "sess_001",
  "execution_id": "exec_001",
  "workflow_name": "Lead-to-Order",
  "agent_name": "Salesforce Agent",
  "agent_type": "CRM",
  "event_type": "agent_started",
  "status": "running",
  "step_name": "Lead Fetch",
  "timestamp": "2026-05-21T10:00:00",
  "latency_ms": 220,
  "metadata": {"source": "salesforce"}
}
```

- Click **Execute**
- See response: `{"success": true, "message": "Telemetry tracked"}`

**Option B: Run test script**

In a new terminal:

```bash
python test_api.py
```

Creates a full workflow: Salesforce → Boomi → D365

## 5. Query Database

```bash
sqlite3 telemetry.db "SELECT agent_name, event_type, status, latency_ms FROM telemetry_logs;"
```

Output:
```
Salesforce Agent|agent_started|running|0
Salesforce Agent|agent_completed|success|250
Boomi Agent|agent_started|running|0
Boomi Agent|agent_completed|success|320
D365 Agent|agent_started|running|0
D365 Agent|agent_completed|success|450
```

## 6. Use in Your Agent

```python
import requests
from datetime import datetime

# Send telemetry
requests.post(
    "http://localhost:8000/api/v1/telemetry",
    json={
        "session_id": "sess_101",
        "execution_id": "exec_101",
        "workflow_name": "Lead-to-Order",
        "agent_name": "Your Agent Name",
        "agent_type": "Integration",
        "event_type": "agent_started",
        "status": "running",
        "step_name": "Your Step",
        "timestamp": datetime.utcnow().isoformat(),
        "latency_ms": 0,
        "metadata": {}
    }
)
```

## File Structure

```
telemetry_sdk/
├── main.py              # FastAPI app
├── test_api.py          # Test script
├── requirements.txt     # Dependencies
├── README.md            # Full docs
├── QUICKSTART.md        # This file
└── telemetry.db         # SQLite (created on first run)
```

## Integration-Specific Adapters

The system includes native adapters for each platform. Instead of transforming data on the client side, send your platform's native telemetry format directly:

### Salesforce Agentforce
```bash
curl -X POST http://127.0.0.1:8000/api/v1/salesforce/telemetry \
  -H "Content-Type: application/json" \
  -d '{"row": {"agent_label__c": "SF Agent", "success_rate__c": 95}}'
```

### Boomi Integration
```bash
curl -X POST http://127.0.0.1:8000/api/v1/boomi/telemetry \
  -H "Content-Type: application/json" \
  -d '{"row": {"process_name": "MyProcess", "execution_duration_ms": 250}}'
```

### Dynamics 365 ERP
```bash
curl -X POST http://127.0.0.1:8000/api/v1/d365/telemetry \
  -H "Content-Type: application/json" \
  -d '{"row": {"entity_type": "Sales Order", "operation_status": "success"}}'
```

### Microsoft 365
```bash
curl -X POST http://127.0.0.1:8000/api/v1/m365/telemetry \
  -H "Content-Type: application/json" \
  -d '{"row": {"workload_type": "SharePoint", "response_time_ms": 200}}'
```

See README.md for complete field mappings for each adapter.

## Next Steps

- Test adapters with `python test_api.py`
- Add more analytics/aggregation endpoints
- Build a dashboard UI
- Add authentication/API keys
- Move to PostgreSQL for production
- Monitor performance across all agents in a single dashboard

## Troubleshooting

**Port 8000 already in use?**
```bash
uvicorn main:app --reload --port 8001
```

**ModuleNotFoundError?**
```bash
pip install -r requirements.txt
```

**Database errors?**
```bash
rm telemetry.db
# Restart server - it will recreate
```
