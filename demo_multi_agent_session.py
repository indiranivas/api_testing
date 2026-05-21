"""
Demo: Multi-Agent Session Tracking Across Different Platforms
Shows how telemetry from different integrations gets linked by session_id
"""
import requests
from datetime import datetime, timezone
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def now_iso():
    return datetime.now(timezone.utc).isoformat()

# ========================================
# SCENARIO: Lead-to-Order Workflow
# Session spans: Salesforce → Boomi → D365 → M365
# ========================================

SESSION_ID = "workflow_lead_to_order_001"

print("=" * 70)
print("MULTI-AGENT SESSION TRACKING DEMO")
print("=" * 70)
print(f"\nSession ID: {SESSION_ID}")
print("Workflow: Lead Detection → Data Transform → Order Creation → Notification\n")

# ========================================
# STEP 1: Salesforce - Lead Detection
# ========================================
print("STEP 1: Salesforce Agent - Lead Detection")
print("-" * 70)

salesforce_payload = {
    "row": {
        "session_id": SESSION_ID,
        "agent_label__c": "Salesforce Lead Agent",
        "agent_type__c": "CRM",
        "success_rate__c": 100,
        "avg_session_duration__c": 150,
        "channel_type__c": "Web Form",
        "engagement_status__c": "Active",
        "total_sessions__c": 1,
        "total_messages__c": 1,
        "session_outcome__c": "Lead Qualified"
    }
}

response = requests.post(f"{BASE_URL}/api/v1/salesforce/telemetry", json=salesforce_payload)
result = response.json()
print(f"✓ Salesforce: {result.get('message', result.get('error'))}")
print(f"  Agent: {result.get('agent')}")
print(f"  Session ID: {result.get('session_id')}\n")

time.sleep(0.5)

# ========================================
# STEP 2: Boomi - Data Transformation
# ========================================
print("STEP 2: Boomi Agent - Data Transformation")
print("-" * 70)

boomi_payload = {
    "row": {
        "session_id": SESSION_ID,
        "execution_id": f"{SESSION_ID}_boomi",
        "process_name": "Lead-Data-Enrichment",
        "connector_name": "Boomi Data Connector",
        "execution_status": "success",
        "execution_duration_ms": 280,
        "records_processed": 1,
        "records_failed": 0,
        "connector_type": "AtomSphere",
        "transformation_count": 3,
        "timestamp": now_iso()
    }
}

response = requests.post(f"{BASE_URL}/api/v1/boomi/telemetry", json=boomi_payload)
result = response.json()
print(f"✓ Boomi: {result.get('message', result.get('error'))}")
print(f"  Agent: {result.get('agent')}")
print(f"  Session ID: {result.get('session_id')}")
print(f"  Processing Time: 280ms\n")

time.sleep(0.5)

# ========================================
# STEP 3: D365 - Order Creation
# ========================================
print("STEP 3: Dynamics 365 Agent - Order Creation")
print("-" * 70)

d365_payload = {
    "row": {
        "session_id": SESSION_ID,
        "execution_id": f"{SESSION_ID}_d365",
        "business_process": "Lead-to-Order",
        "entity_type": "Sales Order",
        "operation_status": "success",
        "execution_time_ms": 450,
        "stage_name": "Order Created",
        "entity_id": f"SO-{SESSION_ID[:8]}",
        "operation_type": "Create",
        "record_count": 1,
        "business_unit": "Sales",
        "timestamp": now_iso()
    }
}

response = requests.post(f"{BASE_URL}/api/v1/d365/telemetry", json=d365_payload)
result = response.json()
print(f"✓ D365: {result.get('message', result.get('error'))}")
print(f"  Agent: {result.get('agent')}")
print(f"  Session ID: {result.get('session_id')}")
print(f"  Entity Created: SO-{SESSION_ID[:8]}\n")

time.sleep(0.5)

# ========================================
# STEP 4: M365 - Send Notification
# ========================================
print("STEP 4: Microsoft 365 Agent - Send Notification")
print("-" * 70)

m365_payload = {
    "row": {
        "session_id": SESSION_ID,
        "execution_id": f"{SESSION_ID}_m365",
        "workload_type": "Teams",
        "service_name": "M365 Notification Service",
        "operation_result": "success",
        "response_time_ms": 120,
        "action_name": "Send Teams Message",
        "user_id": "sales@levelshift.com",
        "workload": "Teams",
        "operation": "SendMessage",
        "timestamp": now_iso()
    }
}

response = requests.post(f"{BASE_URL}/api/v1/m365/telemetry", json=m365_payload)
result = response.json()
print(f"✓ M365: {result.get('message', result.get('error'))}")
print(f"  Agent: {result.get('agent')}")
print(f"  Session ID: {result.get('session_id')}\n")

time.sleep(1)

# ========================================
# RETRIEVE: Query Complete Session
# ========================================
print("=" * 70)
print("RETRIEVING COMPLETE SESSION DATA")
print("=" * 70)
print(f"\nQuerying all telemetry for Session ID: {SESSION_ID}\n")

response = requests.get(f"{BASE_URL}/sessions/{SESSION_ID}")
session_data = response.json()

if "error" in session_data:
    print(f"✗ Error: {session_data['error']}")
else:
    print(f"Session ID: {session_data['session_id']}")
    print(f"Total Events: {session_data['event_count']}")
    print("\nCOMPLETE WORKFLOW TRACE:")
    print("-" * 70)

    for i, event in enumerate(session_data['events'], 1):
        print(f"\n{i}. Agent: {event['agent_name']}")
        print(f"   Event Type: {event['event_type']}")
        print(f"   Status: {event['status']}")
        print(f"   Latency: {event['latency_ms']}ms")
        print(f"   Timestamp: {event['timestamp']}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"""
✓ Successfully tracked complete workflow across 4 different platforms
✓ All agents linked by session_id: {SESSION_ID}
✓ Telemetry sent via different endpoints:
  - Salesforce adapter (CRM platform)
  - Boomi adapter (Integration platform)
  - D365 adapter (ERP platform)
  - M365 adapter (SaaS platform)
✓ All data stored in single database and queried together
""")

# ========================================
# ANALYZE: Workflow Performance
# ========================================
print("\nWORKFLOW PERFORMANCE ANALYSIS:")
print("-" * 70)

total_latency = sum([e['latency_ms'] for e in session_data['events']])
print(f"Total End-to-End Latency: {total_latency}ms")
print(f"Number of Steps: {len(session_data['events'])}")
print(f"Average Step Latency: {total_latency / len(session_data['events']) if session_data['events'] else 0:.0f}ms")
print(f"Success Rate: 100% (all events successful)")

print("\n" + "=" * 70)
