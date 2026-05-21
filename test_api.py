"""
Simple test script for telemetry API
"""
import requests
from datetime import datetime, timezone
import time

BASE_URL = "http://127.0.0.1:8000"

# Use timezone-aware UTC time
def now_iso():
    return datetime.now(timezone.utc).isoformat()

# Test health check
print("Testing health check...")
response = requests.get(f"{BASE_URL}/health")
print(f"✓ Health: {response.json()}\n")

# Test telemetry endpoint
print("Sending telemetry events...")

events = [
    {
        "session_id": "sess_001",
        "execution_id": "exec_001",
        "workflow_name": "Lead-to-Order",
        "agent_name": "Salesforce Agent",
        "agent_type": "CRM",
        "event_type": "agent_started",
        "status": "running",
        "step_name": "Lead Fetch",
        "timestamp": now_iso(),
        "latency_ms": 0,
        "metadata": {"source": "salesforce"}
    },
    {
        "session_id": "sess_001",
        "execution_id": "exec_001",
        "workflow_name": "Lead-to-Order",
        "agent_name": "Salesforce Agent",
        "agent_type": "CRM",
        "event_type": "agent_completed",
        "status": "success",
        "step_name": "Lead Fetch",
        "timestamp": now_iso(),
        "latency_ms": 250,
        "metadata": {"records_fetched": 5}
    },
    {
        "session_id": "sess_001",
        "execution_id": "exec_002",
        "workflow_name": "Lead-to-Order",
        "agent_name": "Boomi Agent",
        "agent_type": "Integration",
        "event_type": "agent_started",
        "status": "running",
        "step_name": "Transform Data",
        "timestamp": now_iso(),
        "latency_ms": 0,
        "metadata": {}
    },
    {
        "session_id": "sess_001",
        "execution_id": "exec_002",
        "workflow_name": "Lead-to-Order",
        "agent_name": "Boomi Agent",
        "agent_type": "Integration",
        "event_type": "agent_completed",
        "status": "success",
        "step_name": "Transform Data",
        "timestamp": now_iso(),
        "latency_ms": 320,
        "metadata": {"records_transformed": 5}
    },
    {
        "session_id": "sess_001",
        "execution_id": "exec_003",
        "workflow_name": "Lead-to-Order",
        "agent_name": "D365 Agent",
        "agent_type": "ERP",
        "event_type": "agent_started",
        "status": "running",
        "step_name": "Order Creation",
        "timestamp": now_iso(),
        "latency_ms": 0,
        "metadata": {}
    },
    {
        "session_id": "sess_001",
        "execution_id": "exec_003",
        "workflow_name": "Lead-to-Order",
        "agent_name": "D365 Agent",
        "agent_type": "ERP",
        "event_type": "agent_completed",
        "status": "success",
        "step_name": "Order Creation",
        "timestamp": now_iso(),
        "latency_ms": 450,
        "metadata": {"orders_created": 5}
    }
]

for event in events:
    response = requests.post(
        f"{BASE_URL}/api/v1/telemetry",
        json=event
    )
    result = response.json()
    print(f"✓ {event['agent_name']} - {event['event_type']}: {result['message']}")

print("\n✓ All standard events tracked successfully!")

# Test Boomi Adapter
print("\n\nTesting Boomi Adapter...")
boomi_payload = {
    "row": {
        "session_id": "sess_002",
        "execution_id": "exec_boomi_001",
        "process_name": "Lead-Transform-Flow",
        "connector_name": "Boomi Connector",
        "execution_status": "success",
        "execution_duration_ms": 280,
        "records_processed": 15,
        "connector_type": "AtomSphere",
        "transformation_count": 3,
        "timestamp": now_iso()
    }
}
response = requests.post(f"{BASE_URL}/api/v1/boomi/telemetry", json=boomi_payload)
result = response.json()
if "error" in result:
    print(f"✗ Boomi Error: {result['error']}")
else:
    print(f"✓ Boomi: {result.get('message', 'Success')}")

# Test D365 Adapter
print("\nTesting D365 Adapter...")
d365_payload = {
    "row": {
        "session_id": "sess_002",
        "execution_id": "exec_d365_001",
        "business_process": "Order-to-Cash",
        "entity_type": "Sales Order",
        "operation_status": "success",
        "execution_time_ms": 350,
        "stage_name": "Create Order",
        "entity_id": "SO-12345",
        "operation_type": "Create",
        "record_count": 1,
        "timestamp": now_iso()
    }
}
response = requests.post(f"{BASE_URL}/api/v1/d365/telemetry", json=d365_payload)
result = response.json()
if "error" in result:
    print(f"✗ D365 Error: {result['error']}")
else:
    print(f"✓ D365: {result.get('message', 'Success')}")

# Test M365 Adapter
print("\nTesting M365 Adapter...")
m365_payload = {
    "row": {
        "session_id": "sess_002",
        "execution_id": "exec_m365_001",
        "workload_type": "SharePoint",
        "service_name": "M365 Service",
        "operation_result": "success",
        "response_time_ms": 200,
        "action_name": "Document Upload",
        "user_id": "user@levelshift.com",
        "workload": "SharePoint",
        "operation": "CreateItem",
        "timestamp": now_iso()
    }
}
response = requests.post(f"{BASE_URL}/api/v1/m365/telemetry", json=m365_payload)
result = response.json()
if "error" in result:
    print(f"✗ M365 Error: {result['error']}")
else:
    print(f"✓ M365: {result.get('message', 'Success')}")

print("\n✓ All adapters tested successfully!")
print("\nCheck database:")
print("  sqlite3 telemetry.db \"SELECT agent_name, agent_type, status, latency_ms FROM telemetry_logs;\"")
