# Telemetry API - SQLite Backend

Minimal FastAPI + SQLite telemetry tracking for LevelShift agents.

## Install

```bash
pip install fastapi uvicorn sqlalchemy
```

Or:

```bash
pip install -r requirements.txt
```

## Run Server

```bash
uvicorn main:app --reload
```

Server starts at: `http://localhost:8000`

API docs: `http://localhost:8000/docs` (Swagger UI)

## Database Schema

SQLite table `telemetry_logs` with fields:

| Field | Type | Index |
|-------|------|-------|
| id | String (UUID) | Primary Key |
| session_id | String | ✓ Indexed |
| execution_id | String | |
| workflow_name | String | |
| agent_name | String | |
| agent_type | String | |
| event_type | String | |
| status | String | |
| step_name | String | |
| timestamp | DateTime | |
| latency_ms | Integer | |
| metadata | JSON | |

## API Endpoint

### POST `/api/v1/telemetry`

Send telemetry event.

**Request:**

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
  "metadata": {
    "source": "salesforce"
  }
}
```

**Response:**

```json
{
  "success": true,
  "message": "Telemetry tracked",
  "session_id": "sess_001"
}
```

## Health Check

### GET `/health`

```bash
curl http://localhost:8000/health
# Response: {"status": "healthy"}
```

## Python Client Example

```python
import requests
from datetime import datetime

payload = {
    "session_id": "sess_101",
    "execution_id": "exec_101",
    "workflow_name": "Lead-to-Order",
    "agent_name": "Boomi Agent",
    "agent_type": "Integration",
    "event_type": "step_completed",
    "status": "success",
    "step_name": "Transform Data",
    "timestamp": datetime.utcnow().isoformat(),
    "latency_ms": 320
}

response = requests.post(
    "http://localhost:8000/api/v1/telemetry",
    json=payload
)

print(response.json())
```

## Database

SQLite file: `telemetry.db` (created automatically)

Query directly:

```bash
sqlite3 telemetry.db "SELECT * FROM telemetry_logs LIMIT 10;"
```

## Test with Swagger

Open: `http://localhost:8000/docs`

Click **POST** `/api/v1/telemetry` → **Try it out** → Paste JSON → **Execute**

## Integration Adapters

The system includes native adapters for each platform to accept telemetry in their native format:

### Salesforce Adapter

**POST** `/api/v1/salesforce/telemetry`

Maps Salesforce Agentforce fields to standard telemetry format.

```json
{
  "row": {
    "agent_label__c": "Salesforce Agent",
    "session_id": "sess_sf_001",
    "success_rate__c": 95,
    "avg_session_duration__c": 250
  }
}
```

### Boomi Adapter

**POST** `/api/v1/boomi/telemetry`

Maps Boomi Integration Platform fields.

```json
{
  "row": {
    "process_name": "Lead-Transform-Flow",
    "connector_name": "Boomi Connector",
    "execution_status": "success",
    "execution_duration_ms": 280,
    "records_processed": 15
  }
}
```

### D365 Adapter

**POST** `/api/v1/d365/telemetry`

Maps Dynamics 365 ERP fields.

```json
{
  "row": {
    "business_process": "Order-to-Cash",
    "entity_type": "Sales Order",
    "operation_status": "success",
    "execution_time_ms": 350,
    "stage_name": "Create Order"
  }
}
```

### M365 Adapter

**POST** `/api/v1/m365/telemetry`

Maps Microsoft 365 audit/activity fields.

```json
{
  "row": {
    "workload_type": "SharePoint",
    "service_name": "M365 Service",
    "operation_result": "success",
    "response_time_ms": 200,
    "action_name": "Document Upload"
  }
}
```

Each adapter transforms platform-specific fields into the standard telemetry schema while preserving all platform-specific data in the `event_metadata` JSON field for detailed analysis.

## Query & Analytics Endpoints

### GET `/sessions/{session_id}`

Get all events for a session.

```bash
curl http://localhost:8000/sessions/sess_001
```

Response includes all events linked by session_id across all agents.

### GET `/sessions/{session_id}/analytics`

Get comprehensive analytics for a session with agent breakdown.

```bash
curl http://localhost:8000/sessions/sess_001/analytics
```

Response includes:
- Total latency and success rate
- Per-agent event count and latency
- Agent breakdown with event details

### GET `/agents/{agent_name}/stats`

Get performance statistics for a specific agent.

```bash
curl http://localhost:8000/agents/Salesforce%20Agent/stats
```

Response includes completed/failed counts, average latency, success rate.

### GET `/workflows/{workflow_name}`

Get all sessions for a workflow.

```bash
curl http://localhost:8000/workflows/Lead-to-Order
```

Response includes all sessions grouped by workflow.

### GET `/workflows/{workflow_name}/summary`

Get summary statistics across all sessions in a workflow.

```bash
curl http://localhost:8000/workflows/Lead-to-Order/summary
```

Response includes:
- Total sessions and agents used
- Overall success rate and latency
- Per-session breakdown

## Multi-Platform Session Tracking

The system automatically connects telemetry from different platforms using `session_id`:

```
Session: workflow_lead_to_order_001
├── Salesforce Agent (CRM)
│   └── Lead Detection (150ms)
├── Boomi Agent (Integration)
│   └── Data Transform (280ms)
├── D365 Agent (ERP)
│   └── Order Creation (450ms)
└── M365 Agent (SaaS)
    └── Send Notification (120ms)
```

All events stored in single database. Query any session to see complete workflow across all platforms.

## Next Steps

- Add authentication (API keys)
- Create dashboard UI
- Migrate to PostgreSQL for production
- Add WebSocket support for real-time streaming
- Add filtering and advanced search endpoints
