from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    DateTime,
    JSON
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import Optional, Dict
import uuid
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Enable CORS for dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Configuration
# -------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./telemetry.db")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# -------------------------
# Helper Functions
# -------------------------
def parse_timestamp(ts):
    """Parse timestamp from various formats to datetime object"""
    if ts is None:
        return datetime.now()
    if isinstance(ts, datetime):
        return ts
    if isinstance(ts, str):
        try:
            # Try ISO format first
            return datetime.fromisoformat(ts.replace('Z', '+00:00'))
        except:
            return datetime.now()
    return datetime.now()
if DATABASE_URL.startswith("sqlite"):
    # SQLite specific configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL and other databases
    engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()

# -------------------------
# Database Model
# -------------------------
class TelemetryLog(Base):
    __tablename__ = "telemetry_logs"
    id = Column(String, primary_key=True)
    session_id = Column(String, index=True)
    execution_id = Column(String)
    workflow_name = Column(String)
    agent_name = Column(String)
    agent_type = Column(String)
    event_type = Column(String)
    status = Column(String)
    step_name = Column(String)
    timestamp = Column(DateTime)
    latency_ms = Column(Integer)
    event_metadata = Column(JSON, nullable=True)

# Create tables
Base.metadata.create_all(bind=engine)

# -------------------------
# Request Model
# -------------------------
class TelemetryPayload(BaseModel):
    session_id: str
    execution_id: str
    workflow_name: str
    agent_name: str
    agent_type: str
    event_type: str
    status: str
    step_name: str
    timestamp: datetime
    latency_ms: Optional[int] = 0
    metadata: Optional[Dict] = None

# -------------------------
# API Endpoint
# -------------------------
@app.post("/api/v1/telemetry")
async def track_telemetry(payload: TelemetryPayload):
    db = SessionLocal()
    try:
        telemetry = TelemetryLog(
            id=str(uuid.uuid4()),
            session_id=payload.session_id,
            execution_id=payload.execution_id,
            workflow_name=payload.workflow_name,
            agent_name=payload.agent_name,
            agent_type=payload.agent_type,
            event_type=payload.event_type,
            status=payload.status,
            step_name=payload.step_name,
            timestamp=payload.timestamp,
            latency_ms=payload.latency_ms,
            event_metadata=payload.metadata
        )
        db.add(telemetry)
        db.commit()
        return {
            "success": True,
            "message": "Telemetry tracked",
            "session_id": payload.session_id
        }
    finally:
        db.close()

# -------------------------
# Query Endpoints
# -------------------------
@app.get("/sessions/{session_id}")
def get_session_events(session_id: str):
    """Get all events for a session"""
    db = SessionLocal()
    try:
        events = db.query(TelemetryLog).filter(
            TelemetryLog.session_id == session_id
        ).all()

        if not events:
            return {"error": "Session not found", "session_id": session_id}

        return {
            "session_id": session_id,
            "event_count": len(events),
            "events": [
                {
                    "id": e.id,
                    "agent_name": e.agent_name,
                    "event_type": e.event_type,
                    "status": e.status,
                    "step_name": e.step_name,
                    "latency_ms": e.latency_ms,
                    "timestamp": e.timestamp.isoformat() if e.timestamp else None,
                }
                for e in events
            ]
        }
    finally:
        db.close()


@app.get("/agents/{agent_name}/stats")
def get_agent_stats(agent_name: str):
    """Get performance stats for an agent"""
    db = SessionLocal()
    try:
        events = db.query(TelemetryLog).filter(
            TelemetryLog.agent_name == agent_name
        ).all()

        if not events:
            return {"error": "Agent not found", "agent_name": agent_name}

        completed = [e for e in events if e.event_type == "agent_completed"]
        failed = [e for e in events if e.event_type == "agent_failed"]

        total_latency = sum([e.latency_ms or 0 for e in completed])
        avg_latency = total_latency / len(completed) if completed else 0

        return {
            "agent_name": agent_name,
            "total_events": len(events),
            "completed": len(completed),
            "failed": len(failed),
            "avg_latency_ms": round(avg_latency, 2),
            "total_latency_ms": total_latency,
            "success_rate": round((len(completed) / len(events) * 100), 2) if events else 0
        }
    finally:
        db.close()


@app.get("/workflows/{workflow_name}")
def get_workflow_sessions(workflow_name: str):
    """Get all sessions for a workflow"""
    db = SessionLocal()
    try:
        # Get all events for this workflow
        events = db.query(TelemetryLog).filter(
            TelemetryLog.workflow_name == workflow_name
        ).all()

        if not events:
            return {"error": "Workflow not found", "workflow_name": workflow_name}

        # Group by session_id
        sessions = {}
        for event in events:
            if event.session_id not in sessions:
                sessions[event.session_id] = {
                    "session_id": event.session_id,
                    "workflow_name": workflow_name,
                    "events": [],
                    "total_latency_ms": 0,
                    "agent_count": set()
                }
            sessions[event.session_id]["events"].append({
                "agent_name": event.agent_name,
                "event_type": event.event_type,
                "status": event.status,
                "latency_ms": event.latency_ms
            })
            sessions[event.session_id]["total_latency_ms"] += event.latency_ms or 0
            sessions[event.session_id]["agent_count"].add(event.agent_name)

        # Convert set to list for JSON serialization
        for session in sessions.values():
            session["agent_count"] = list(session["agent_count"])

        return {
            "workflow_name": workflow_name,
            "session_count": len(sessions),
            "sessions": list(sessions.values())
        }
    finally:
        db.close()


# -------------------------
# Salesforce Adapter
# -------------------------
@app.post("/api/v1/salesforce/telemetry")
async def salesforce_telemetry(payload: dict):
    """Salesforce Agentforce telemetry adapter"""
    # Extract from Salesforce row format
    try:
        # Map Salesforce fields → standard telemetry
        row = payload.get("row", {})

        telemetry_data = {
            "session_id": row.get("session_id") or str(uuid.uuid4()),
            "execution_id": row.get("execution_id") or str(uuid.uuid4()),
            "workflow_name": "Salesforce-Workflow",
            "agent_name": row.get("agent_label__c", "Salesforce Agent"),
            "agent_type": row.get("agent_type__c", "Salesforce"),
            "event_type": "agent_completed",
            "status": "success" if row.get("success_rate__c", 0) > 80 else "partial",
            "step_name": row.get("action_label__c", "Agent Action"),
            "timestamp": row.get("session_date__c", datetime.now(datetime.UTC).isoformat()),
            "latency_ms": int(row.get("avg_session_duration__c", 0) or 0),
            "event_metadata": {
                "channel": row.get("channel_type__c"),
                "engagement_status": row.get("engagement_status__c"),
                "total_sessions": row.get("total_sessions__c"),
                "engagement_rate": row.get("engagement_rate__c"),
                "success_rate": row.get("success_rate__c"),
                "total_messages": row.get("total_messages__c"),
                "total_interactions": row.get("total_interactions__c"),
                "deflection_rate": row.get("deflection_rate__c"),
                "escalation_rate": row.get("escalation_rate__c"),
                "user_feedback_status": row.get("user_feedback_status__c"),
                "session_outcome": row.get("session_outcome__c"),
            }
        }

        # Insert into database
        db = SessionLocal()
        try:
            telemetry = TelemetryLog(
                id=str(uuid.uuid4()),
                session_id=telemetry_data["session_id"],
                execution_id=telemetry_data["execution_id"],
                workflow_name=telemetry_data["workflow_name"],
                agent_name=telemetry_data["agent_name"],
                agent_type=telemetry_data["agent_type"],
                event_type=telemetry_data["event_type"],
                status=telemetry_data["status"],
                step_name=telemetry_data["step_name"],
                timestamp=telemetry_data["timestamp"],
                latency_ms=telemetry_data["latency_ms"],
                event_metadata=telemetry_data.get("event_metadata")
            )
            db.add(telemetry)
            db.commit()
            return {
                "success": True,
                "message": "Salesforce telemetry ingested",
                "agent": telemetry_data["agent_name"],
                "session_id": telemetry_data["session_id"]
            }
        finally:
            db.close()

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# -------------------------
# Boomi Adapter
# -------------------------
@app.post("/api/v1/boomi/telemetry")
async def boomi_telemetry(payload: dict):
    """Boomi Integration Platform telemetry adapter"""
    try:
        # Map Boomi fields → standard telemetry
        row = payload.get("row", {})

        telemetry_data = {
            "session_id": row.get("session_id") or str(uuid.uuid4()),
            "execution_id": row.get("execution_id") or str(uuid.uuid4()),
            "workflow_name": row.get("process_name", "Boomi-Process"),
            "agent_name": row.get("connector_name", "Boomi Agent"),
            "agent_type": "Integration",
            "event_type": "agent_completed",
            "status": row.get("execution_status", "unknown"),
            "step_name": row.get("step_name", "Process Execution"),
            "timestamp": parse_timestamp(row.get("timestamp") or row.get("execution_time")),
            "latency_ms": int(row.get("execution_duration_ms", 0) or 0),
            "event_metadata": {
                "connector_type": row.get("connector_type"),
                "records_processed": row.get("records_processed"),
                "records_failed": row.get("records_failed"),
                "error_message": row.get("error_message"),
                "execution_environment": row.get("execution_environment"),
                "transformation_count": row.get("transformation_count"),
                "process_version": row.get("process_version"),
            }
        }

        # Insert into database
        db = SessionLocal()
        try:
            telemetry = TelemetryLog(
                id=str(uuid.uuid4()),
                session_id=telemetry_data["session_id"],
                execution_id=telemetry_data["execution_id"],
                workflow_name=telemetry_data["workflow_name"],
                agent_name=telemetry_data["agent_name"],
                agent_type=telemetry_data["agent_type"],
                event_type=telemetry_data["event_type"],
                status=telemetry_data["status"],
                step_name=telemetry_data["step_name"],
                timestamp=telemetry_data["timestamp"],
                latency_ms=telemetry_data["latency_ms"],
                event_metadata=telemetry_data.get("event_metadata")
            )
            db.add(telemetry)
            db.commit()
            return {
                "success": True,
                "message": "Boomi telemetry ingested",
                "agent": telemetry_data["agent_name"],
                "session_id": telemetry_data["session_id"]
            }
        finally:
            db.close()

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# -------------------------
# D365 Adapter
# -------------------------
@app.post("/api/v1/d365/telemetry")
async def d365_telemetry(payload: dict):
    """Dynamics 365 ERP telemetry adapter"""
    try:
        # Map D365 fields → standard telemetry
        row = payload.get("row", {})

        telemetry_data = {
            "session_id": row.get("session_id") or str(uuid.uuid4()),
            "execution_id": row.get("execution_id") or str(uuid.uuid4()),
            "workflow_name": row.get("business_process", "D365-Workflow"),
            "agent_name": row.get("entity_type", "D365 Agent"),
            "agent_type": "ERP",
            "event_type": "agent_completed",
            "status": row.get("operation_status", "unknown"),
            "step_name": row.get("stage_name", "Process Stage"),
            "timestamp": parse_timestamp(row.get("timestamp") or row.get("created_on")),
            "latency_ms": int(row.get("execution_time_ms", 0) or 0),
            "event_metadata": {
                "entity_id": row.get("entity_id"),
                "operation_type": row.get("operation_type"),
                "organization_id": row.get("organization_id"),
                "user_id": row.get("user_id"),
                "record_count": row.get("record_count"),
                "error_code": row.get("error_code"),
                "business_unit": row.get("business_unit"),
                "process_stage": row.get("process_stage"),
            }
        }

        # Insert into database
        db = SessionLocal()
        try:
            telemetry = TelemetryLog(
                id=str(uuid.uuid4()),
                session_id=telemetry_data["session_id"],
                execution_id=telemetry_data["execution_id"],
                workflow_name=telemetry_data["workflow_name"],
                agent_name=telemetry_data["agent_name"],
                agent_type=telemetry_data["agent_type"],
                event_type=telemetry_data["event_type"],
                status=telemetry_data["status"],
                step_name=telemetry_data["step_name"],
                timestamp=telemetry_data["timestamp"],
                latency_ms=telemetry_data["latency_ms"],
                event_metadata=telemetry_data.get("event_metadata")
            )
            db.add(telemetry)
            db.commit()
            return {
                "success": True,
                "message": "D365 telemetry ingested",
                "agent": telemetry_data["agent_name"],
                "session_id": telemetry_data["session_id"]
            }
        finally:
            db.close()

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# -------------------------
# M365 Adapter
# -------------------------
@app.post("/api/v1/m365/telemetry")
async def m365_telemetry(payload: dict):
    """Microsoft 365 telemetry adapter"""
    try:
        # Map M365 fields → standard telemetry
        row = payload.get("row", {})

        telemetry_data = {
            "session_id": row.get("session_id") or str(uuid.uuid4()),
            "execution_id": row.get("execution_id") or str(uuid.uuid4()),
            "workflow_name": row.get("workload_type", "M365-Workflow"),
            "agent_name": row.get("service_name", "M365 Agent"),
            "agent_type": "SaaS",
            "event_type": "agent_completed",
            "status": row.get("operation_result", "unknown"),
            "step_name": row.get("action_name", "M365 Operation"),
            "timestamp": parse_timestamp(row.get("timestamp") or row.get("activity_datetime")),
            "latency_ms": int(row.get("response_time_ms", 0) or 0),
            "event_metadata": {
                "user_id": row.get("user_id"),
                "workload": row.get("workload"),
                "object_id": row.get("object_id"),
                "operation": row.get("operation"),
                "client_ip": row.get("client_ip"),
                "user_agent": row.get("user_agent"),
                "result_status": row.get("result_status"),
                "audit_record_type": row.get("audit_record_type"),
            }
        }

        # Insert into database
        db = SessionLocal()
        try:
            telemetry = TelemetryLog(
                id=str(uuid.uuid4()),
                session_id=telemetry_data["session_id"],
                execution_id=telemetry_data["execution_id"],
                workflow_name=telemetry_data["workflow_name"],
                agent_name=telemetry_data["agent_name"],
                agent_type=telemetry_data["agent_type"],
                event_type=telemetry_data["event_type"],
                status=telemetry_data["status"],
                step_name=telemetry_data["step_name"],
                timestamp=telemetry_data["timestamp"],
                latency_ms=telemetry_data["latency_ms"],
                event_metadata=telemetry_data.get("event_metadata")
            )
            db.add(telemetry)
            db.commit()
            return {
                "success": True,
                "message": "M365 telemetry ingested",
                "agent": telemetry_data["agent_name"],
                "session_id": telemetry_data["session_id"]
            }
        finally:
            db.close()

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# -------------------------
# Session Analytics
# -------------------------
@app.get("/sessions/{session_id}/analytics")
def get_session_analytics(session_id: str):
    """Get comprehensive analytics for a session"""
    db = SessionLocal()
    try:
        events = db.query(TelemetryLog).filter(
            TelemetryLog.session_id == session_id
        ).order_by(TelemetryLog.timestamp).all()

        if not events:
            return {"error": "Session not found", "session_id": session_id}

        # Group by agent
        agents = {}
        for event in events:
            if event.agent_name not in agents:
                agents[event.agent_name] = {
                    "agent_name": event.agent_name,
                    "agent_type": event.agent_type,
                    "event_count": 0,
                    "total_latency_ms": 0,
                    "success_count": 0,
                    "error_count": 0,
                    "events": []
                }

            agents[event.agent_name]["event_count"] += 1
            agents[event.agent_name]["total_latency_ms"] += event.latency_ms or 0

            if event.status == "success":
                agents[event.agent_name]["success_count"] += 1
            else:
                agents[event.agent_name]["error_count"] += 1

            agents[event.agent_name]["events"].append({
                "event_type": event.event_type,
                "status": event.status,
                "latency_ms": event.latency_ms,
                "timestamp": event.timestamp.isoformat() if event.timestamp else None
            })

        # Calculate totals
        total_latency = sum([e.latency_ms or 0 for e in events])
        success_events = [e for e in events if e.status == "success"]
        error_events = [e for e in events if e.status != "success"]

        return {
            "session_id": session_id,
            "workflow_name": events[0].workflow_name if events else "Unknown",
            "total_events": len(events),
            "unique_agents": len(agents),
            "total_latency_ms": total_latency,
            "avg_latency_ms": round(total_latency / len(events), 2) if events else 0,
            "success_events": len(success_events),
            "error_events": len(error_events),
            "success_rate": round((len(success_events) / len(events) * 100), 2) if events else 0,
            "start_time": events[0].timestamp.isoformat() if events else None,
            "end_time": events[-1].timestamp.isoformat() if events else None,
            "agents": list(agents.values())
        }
    finally:
        db.close()


# -------------------------
# Workflow Summary
# -------------------------
@app.get("/workflows/{workflow_name}/summary")
def get_workflow_summary(workflow_name: str):
    """Get summary statistics for all sessions in a workflow"""
    db = SessionLocal()
    try:
        events = db.query(TelemetryLog).filter(
            TelemetryLog.workflow_name == workflow_name
        ).all()

        if not events:
            return {"error": "Workflow not found", "workflow_name": workflow_name}

        # Group by session
        sessions = {}
        agents_used = set()

        for event in events:
            agents_used.add(event.agent_name)
            if event.session_id not in sessions:
                sessions[event.session_id] = {
                    "session_id": event.session_id,
                    "event_count": 0,
                    "agent_count": set(),
                    "total_latency_ms": 0,
                    "success": 0,
                    "failed": 0
                }

            sessions[event.session_id]["event_count"] += 1
            sessions[event.session_id]["agent_count"].add(event.agent_name)
            sessions[event.session_id]["total_latency_ms"] += event.latency_ms or 0

            if event.status == "success":
                sessions[event.session_id]["success"] += 1
            else:
                sessions[event.session_id]["failed"] += 1

        # Convert sets to lists for JSON serialization
        for session in sessions.values():
            session["agent_count"] = list(session["agent_count"])

        # Calculate workflow stats
        total_events = len(events)
        success_events = len([e for e in events if e.status == "success"])
        total_latency = sum([e.latency_ms or 0 for e in events])

        return {
            "workflow_name": workflow_name,
            "total_sessions": len(sessions),
            "unique_agents": list(agents_used),
            "agent_count": len(agents_used),
            "total_events": total_events,
            "success_rate": round((success_events / total_events * 100), 2) if total_events else 0,
            "avg_latency_ms": round(total_latency / total_events, 2) if total_events else 0,
            "sessions": list(sessions.values())
        }
    finally:
        db.close()


# -------------------------
# Health Check
# -------------------------
@app.get("/health")
def health():
    return {"status": "healthy"}


# -------------------------
# Serve Static Files (for production deployment)
# -------------------------
from fastapi.staticfiles import StaticFiles
import pathlib

# Try to serve static files if they exist
static_dir = pathlib.Path(__file__).parent
html_files = ["index.html", "test.html", "dashboard.html"]

for html_file in html_files:
    file_path = static_dir / html_file
    if file_path.exists():
        # Mount static files at the end
        break

# Mount static files directory
try:
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
except Exception as e:
    if DEBUG:
        print(f"Warning: Could not mount static files: {e}")
