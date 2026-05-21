# Multi-Agent Session Tracking Guide

Complete guide to tracking workflows across multiple integration platforms.

## Quick Start

### 1. Start the Server

```bash
uvicorn main:app --reload
```

### 2. Run the Multi-Agent Demo

In a new terminal:

```bash
python demo_multi_agent_session.py
```

This will:
- Send telemetry from 4 different platforms (Salesforce, Boomi, D365, M365)
- All linked by the same `session_id`
- Query the database to show the complete workflow
- Display analytics and performance metrics

## How It Works

### Session Linking

All telemetry events are connected using `session_id`:

```
┌─ Session: workflow_lead_to_order_001 ──────────────────┐
│                                                         │
│  Salesforce Agent (CRM)           Latency: 150ms       │
│  └─ Lead Detection                Status: success      │
│                                                         │
│  Boomi Agent (Integration)        Latency: 280ms       │
│  └─ Data Transform                Status: success      │
│                                                         │
│  D365 Agent (ERP)                 Latency: 450ms       │
│  └─ Order Creation                Status: success      │
│                                                         │
│  M365 Agent (SaaS)                Latency: 120ms       │
│  └─ Send Notification             Status: success      │
│                                                         │
│  Total: 1000ms end-to-end                              │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

```
1. Salesforce Agentforce sends telemetry via:
   POST /api/v1/salesforce/telemetry
   └─ Receives native Salesforce field format
   └─ Maps to standard telemetry schema
   └─ Stores with session_id = workflow_001

2. Boomi sends telemetry via:
   POST /api/v1/boomi/telemetry
   └─ Receives native Boomi field format
   └─ Maps to standard telemetry schema
   └─ Stores with session_id = workflow_001

3. D365 sends telemetry via:
   POST /api/v1/d365/telemetry
   └─ Receives native D365 field format
   └─ Maps to standard telemetry schema
   └─ Stores with session_id = workflow_001

4. M365 sends telemetry via:
   POST /api/v1/m365/telemetry
   └─ Receives native M365 field format
   └─ Maps to standard telemetry schema
   └─ Stores with session_id = workflow_001

5. Query complete session:
   GET /sessions/workflow_001
   └─ Returns all 4+ events linked by session_id
   └─ Shows complete workflow trace
```

## Scenarios

### Scenario 1: Lead to Order

```
Session: lead_to_order_001

1. Lead comes in via Salesforce
   Platform: Salesforce
   Agent: Salesforce Lead Agent
   Event: agent_completed
   Status: success
   Latency: 150ms

2. Data enriched in Boomi
   Platform: Boomi
   Agent: Boomi Data Connector
   Event: agent_completed
   Status: success
   Latency: 280ms

3. Order created in D365
   Platform: D365
   Agent: D365 ERP
   Event: agent_completed
   Status: success
   Latency: 450ms

4. Notification sent via M365
   Platform: M365
   Agent: M365 Teams Service
   Event: agent_completed
   Status: success
   Latency: 120ms

Total Workflow Time: 1000ms
Success Rate: 100%
Agents Involved: 4
```

### Scenario 2: Support Ticket Resolution

```
Session: support_ticket_001

1. Ticket created in Salesforce
   Platform: Salesforce
   Status: received

2. AI Analysis via Boomi
   Platform: Boomi
   Status: analyzed

3. Escalation to D365 if needed
   Platform: D365
   Status: created

4. Team notification via M365
   Platform: M365
   Status: notified
```

## API Usage

### Send Telemetry from Each Platform

#### Salesforce Agentforce

```python
import requests

payload = {
    "row": {
        "session_id": "workflow_001",
        "agent_label__c": "Salesforce Agent",
        "success_rate__c": 95,
        "avg_session_duration__c": 150
    }
}

requests.post(
    "http://localhost:8000/api/v1/salesforce/telemetry",
    json=payload
)
```

#### Boomi

```python
payload = {
    "row": {
        "session_id": "workflow_001",
        "process_name": "Lead-Transform",
        "connector_name": "Boomi Connector",
        "execution_status": "success",
        "execution_duration_ms": 280
    }
}

requests.post(
    "http://localhost:8000/api/v1/boomi/telemetry",
    json=payload
)
```

#### Dynamics 365

```python
payload = {
    "row": {
        "session_id": "workflow_001",
        "business_process": "Lead-to-Order",
        "entity_type": "Sales Order",
        "operation_status": "success",
        "execution_time_ms": 450
    }
}

requests.post(
    "http://localhost:8000/api/v1/d365/telemetry",
    json=payload
)
```

#### Microsoft 365

```python
payload = {
    "row": {
        "session_id": "workflow_001",
        "workload_type": "Teams",
        "service_name": "M365 Service",
        "operation_result": "success",
        "response_time_ms": 120
    }
}

requests.post(
    "http://localhost:8000/api/v1/m365/telemetry",
    json=payload
)
```

### Query the Session

```python
import requests

# Get all events in session
response = requests.get(
    "http://localhost:8000/sessions/workflow_001"
)
events = response.json()

# Get analytics
response = requests.get(
    "http://localhost:8000/sessions/workflow_001/analytics"
)
analytics = response.json()

# Get workflow summary
response = requests.get(
    "http://localhost:8000/workflows/Lead-to-Order/summary"
)
summary = response.json()
```

## Key Concepts

### Session ID

Unique identifier linking all related events:
```
session_id: "workflow_lead_to_order_001"
```

All events with this session_id are part of the same workflow, regardless of platform.

### Agent Name

Identifies which platform/connector generated the event:
- Salesforce Agent
- Boomi Agent
- D365 Agent
- M365 Agent

### Event Type

What happened:
- `agent_started` - Agent began processing
- `agent_completed` - Agent finished successfully
- `agent_failed` - Agent encountered error

### Status

Result of the event:
- `success` - Completed successfully
- `error` - Failed with error
- `partial` - Partially successful
- `running` - Currently processing

### Latency (latency_ms)

Time taken for the event in milliseconds.

### Event Metadata

Platform-specific data stored as JSON:
```json
{
  "channel_type": "Web",
  "engagement_status": "Active",
  "records_processed": 15,
  "error_message": null
}
```

## Analytics Available

### Per-Session Analytics

```bash
GET /sessions/{session_id}/analytics
```

Returns:
- Total events and unique agents
- Total end-to-end latency
- Success/error counts
- Per-agent breakdown
- Event timeline with timestamps

### Per-Agent Statistics

```bash
GET /agents/{agent_name}/stats
```

Returns:
- Agent's total events
- Completed vs failed counts
- Average latency
- Success rate

### Per-Workflow Summary

```bash
GET /workflows/{workflow_name}/summary
```

Returns:
- Total sessions in workflow
- Unique agents used
- Overall success rate
- Average latency
- Per-session breakdown

## Database Query

View raw data in SQLite:

```bash
sqlite3 telemetry.db

# View all events in a session
SELECT * FROM telemetry_logs WHERE session_id = 'workflow_001';

# View events by agent
SELECT agent_name, COUNT(*) FROM telemetry_logs GROUP BY agent_name;

# View events by workflow
SELECT workflow_name, COUNT(*) FROM telemetry_logs GROUP BY workflow_name;

# Calculate average latency by agent
SELECT agent_name, AVG(latency_ms) FROM telemetry_logs GROUP BY agent_name;
```

## Troubleshooting

### Session not showing all events

Ensure all requests use the **same** `session_id`:
```python
# ✓ Correct - all same session
{"row": {"session_id": "workflow_001", ...}}
{"row": {"session_id": "workflow_001", ...}}

# ✗ Wrong - different sessions
{"row": {"session_id": "workflow_001", ...}}
{"row": {"session_id": "workflow_002", ...}}
```

### Events showing up separately

Check that events are being sent to the correct endpoints:
- Salesforce → `/api/v1/salesforce/telemetry`
- Boomi → `/api/v1/boomi/telemetry`
- D365 → `/api/v1/d365/telemetry`
- M365 → `/api/v1/m365/telemetry`

### Query returns empty

Make sure `session_id` in query matches what was sent:
```bash
# If you sent with session_id = "workflow_001"
GET /sessions/workflow_001  # ✓ Correct

# Not this
GET /sessions/workflow_002  # ✗ Wrong
```

## Next Steps

1. **Run the demo**: `python demo_multi_agent_session.py`
2. **Query the session**: `curl http://localhost:8000/sessions/workflow_lead_to_order_001/analytics`
3. **Integrate with your agents**: Send telemetry from each platform
4. **Monitor workflows**: Use analytics endpoints to track performance
5. **Build dashboards**: Use query endpoints to create custom views

---

See `API_REFERENCE.md` for complete endpoint documentation.
