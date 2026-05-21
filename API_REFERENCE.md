# Telemetry API Reference

Complete guide to all telemetry endpoints for multi-platform agent tracking.

## Overview

The Telemetry API collects telemetry data from multiple integration platforms (Salesforce, Boomi, D365, M365) and automatically connects them using `session_id`. Query any session to see the complete workflow across all platforms.

## Base URL

```
http://localhost:8000
```

## Telemetry Ingestion Endpoints

### 1. Generic Telemetry Endpoint

**POST** `/api/v1/telemetry`

Send telemetry in standard format.

**Request:**
```json
{
  "session_id": "sess_001",
  "execution_id": "exec_001",
  "workflow_name": "Lead-to-Order",
  "agent_name": "Custom Agent",
  "agent_type": "Custom",
  "event_type": "agent_completed",
  "status": "success",
  "step_name": "Process Step",
  "timestamp": "2026-05-21T10:00:00Z",
  "latency_ms": 250,
  "metadata": {"custom_field": "value"}
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

---

### 2. Salesforce Agentforce Adapter

**POST** `/api/v1/salesforce/telemetry`

Send Salesforce Agentforce telemetry in native format.

**Request:**
```json
{
  "row": {
    "session_id": "sess_sf_001",
    "agent_label__c": "Salesforce Agent",
    "agent_type__c": "CRM",
    "success_rate__c": 95,
    "avg_session_duration__c": 250,
    "channel_type__c": "Web",
    "engagement_status__c": "Active",
    "total_sessions__c": 1,
    "engagement_rate__c": 85,
    "deflection_rate__c": 15,
    "escalation_rate__c": 5,
    "session_outcome__c": "Resolved"
  }
}
```

**Field Mappings:**
- `agent_label__c` → agent_name
- `agent_type__c` → agent_type
- `success_rate__c` → status determination
- `avg_session_duration__c` → latency_ms

---

### 3. Boomi Integration Adapter

**POST** `/api/v1/boomi/telemetry`

Send Boomi Integration Platform telemetry in native format.

**Request:**
```json
{
  "row": {
    "session_id": "sess_boomi_001",
    "process_name": "Lead-Transform",
    "connector_name": "Boomi Connector",
    "execution_status": "success",
    "execution_duration_ms": 280,
    "records_processed": 15,
    "records_failed": 0,
    "connector_type": "AtomSphere",
    "transformation_count": 3,
    "error_message": null
  }
}
```

**Field Mappings:**
- `process_name` → workflow_name
- `connector_name` → agent_name
- `execution_status` → status
- `execution_duration_ms` → latency_ms

---

### 4. Dynamics 365 ERP Adapter

**POST** `/api/v1/d365/telemetry`

Send Dynamics 365 telemetry in native format.

**Request:**
```json
{
  "row": {
    "session_id": "sess_d365_001",
    "business_process": "Order-to-Cash",
    "entity_type": "Sales Order",
    "operation_status": "success",
    "execution_time_ms": 350,
    "stage_name": "Order Created",
    "entity_id": "SO-12345",
    "operation_type": "Create",
    "record_count": 1,
    "business_unit": "Sales",
    "organization_id": "org_001"
  }
}
```

**Field Mappings:**
- `business_process` → workflow_name
- `entity_type` → agent_name
- `operation_status` → status
- `execution_time_ms` → latency_ms

---

### 5. Microsoft 365 Adapter

**POST** `/api/v1/m365/telemetry`

Send Microsoft 365 (Teams, SharePoint, etc.) telemetry in native format.

**Request:**
```json
{
  "row": {
    "session_id": "sess_m365_001",
    "workload_type": "SharePoint",
    "service_name": "M365 Service",
    "operation_result": "success",
    "response_time_ms": 200,
    "action_name": "Document Upload",
    "user_id": "user@company.com",
    "workload": "SharePoint",
    "operation": "CreateItem",
    "audit_record_type": "SharePointFileOperation"
  }
}
```

**Field Mappings:**
- `workload_type` → workflow_name
- `service_name` → agent_name
- `operation_result` → status
- `response_time_ms` → latency_ms

---

## Query Endpoints

### 1. Get Session Events

**GET** `/sessions/{session_id}`

Retrieve all events for a session across all agents.

**Example:**
```bash
curl http://localhost:8000/sessions/sess_001
```

**Response:**
```json
{
  "session_id": "sess_001",
  "event_count": 4,
  "events": [
    {
      "id": "uuid-1",
      "agent_name": "Salesforce Agent",
      "event_type": "agent_completed",
      "status": "success",
      "step_name": "Lead Detection",
      "latency_ms": 150,
      "timestamp": "2026-05-21T10:00:00Z"
    },
    {
      "id": "uuid-2",
      "agent_name": "Boomi Agent",
      "event_type": "agent_completed",
      "status": "success",
      "step_name": "Data Transform",
      "latency_ms": 280,
      "timestamp": "2026-05-21T10:00:01Z"
    }
  ]
}
```

---

### 2. Get Session Analytics

**GET** `/sessions/{session_id}/analytics`

Get comprehensive analytics for a session with agent breakdown.

**Example:**
```bash
curl http://localhost:8000/sessions/sess_001/analytics
```

**Response:**
```json
{
  "session_id": "sess_001",
  "workflow_name": "Lead-to-Order",
  "total_events": 4,
  "unique_agents": 4,
  "total_latency_ms": 1100,
  "avg_latency_ms": 275,
  "success_events": 4,
  "error_events": 0,
  "success_rate": 100.0,
  "start_time": "2026-05-21T10:00:00Z",
  "end_time": "2026-05-21T10:00:04Z",
  "agents": [
    {
      "agent_name": "Salesforce Agent",
      "agent_type": "CRM",
      "event_count": 1,
      "total_latency_ms": 150,
      "success_count": 1,
      "error_count": 0,
      "events": [
        {
          "event_type": "agent_completed",
          "status": "success",
          "latency_ms": 150,
          "timestamp": "2026-05-21T10:00:00Z"
        }
      ]
    }
  ]
}
```

---

### 3. Get Agent Statistics

**GET** `/agents/{agent_name}/stats`

Get performance statistics for a specific agent across all sessions.

**Example:**
```bash
curl http://localhost:8000/agents/Salesforce%20Agent/stats
```

**Response:**
```json
{
  "agent_name": "Salesforce Agent",
  "total_events": 5,
  "completed": 5,
  "failed": 0,
  "avg_latency_ms": 160.5,
  "total_latency_ms": 802,
  "success_rate": 100.0
}
```

---

### 4. Get Workflow Sessions

**GET** `/workflows/{workflow_name}`

Get all sessions for a workflow.

**Example:**
```bash
curl http://localhost:8000/workflows/Lead-to-Order
```

**Response:**
```json
{
  "workflow_name": "Lead-to-Order",
  "session_count": 2,
  "sessions": [
    {
      "session_id": "sess_001",
      "workflow_name": "Lead-to-Order",
      "events": [...],
      "total_latency_ms": 1100,
      "agent_count": ["Salesforce Agent", "Boomi Agent", "D365 Agent", "M365 Agent"]
    }
  ]
}
```

---

### 5. Get Workflow Summary

**GET** `/workflows/{workflow_name}/summary`

Get summary statistics across all sessions in a workflow.

**Example:**
```bash
curl http://localhost:8000/workflows/Lead-to-Order/summary
```

**Response:**
```json
{
  "workflow_name": "Lead-to-Order",
  "total_sessions": 10,
  "unique_agents": 4,
  "agent_count": 4,
  "total_events": 40,
  "success_rate": 95.0,
  "avg_latency_ms": 270.5,
  "sessions": [
    {
      "session_id": "sess_001",
      "event_count": 4,
      "agent_count": ["Salesforce Agent", "Boomi Agent", "D365 Agent", "M365 Agent"],
      "total_latency_ms": 1100,
      "success": 4,
      "failed": 0
    }
  ]
}
```

---

## Health Check

**GET** `/health`

Simple health check endpoint.

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy"
}
```

---

## Multi-Platform Session Tracking Example

### Scenario: Lead-to-Order Workflow

A single workflow where telemetry flows through multiple platforms:

```
1. Salesforce detects a new lead
   POST /api/v1/salesforce/telemetry
   session_id: workflow_001

2. Boomi transforms the data
   POST /api/v1/boomi/telemetry
   session_id: workflow_001

3. D365 creates an order
   POST /api/v1/d365/telemetry
   session_id: workflow_001

4. M365 sends a notification
   POST /api/v1/m365/telemetry
   session_id: workflow_001
```

### Query the Complete Workflow

```bash
# Get all events in the session
curl http://localhost:8000/sessions/workflow_001

# Get detailed analytics
curl http://localhost:8000/sessions/workflow_001/analytics

# See all sessions in this workflow
curl http://localhost:8000/workflows/Lead-to-Order

# Get workflow summary statistics
curl http://localhost:8000/workflows/Lead-to-Order/summary
```

---

## Key Features

✅ **Multi-Platform Support**: Collect telemetry from Salesforce, Boomi, D365, M365, and custom agents

✅ **Session-Based Linking**: All telemetry connected by `session_id`

✅ **Flexible Metadata**: Platform-specific data stored in `event_metadata` JSON field

✅ **Real-Time Analytics**: Query endpoints for immediate insights

✅ **Cross-Platform Queries**: See complete workflows across all integrations

✅ **Performance Metrics**: Track latency, success rates, and agent efficiency

---

## Status Codes

- `200` - Success
- `400` - Bad Request
- `404` - Not Found
- `500` - Server Error

---

## Database

Data stored in SQLite at `telemetry.db`

Tables:
- `telemetry_logs` - All telemetry events

Indexes:
- `session_id` - Fast session lookups
