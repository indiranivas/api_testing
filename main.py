from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict
import pathlib

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (simple for now)
telemetry_store = []

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
    timestamp: str
    latency_ms: int = 0
    metadata: Optional[Dict] = None

# -------------------------
# API Endpoints
# -------------------------

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "telemetry-system"}

@app.post("/api/v1/telemetry")
async def track_telemetry(payload: TelemetryPayload):
    """Track a telemetry event"""
    try:
        event_data = {
            "id": str(__import__("uuid").uuid4()),
            "session_id": payload.session_id,
            "execution_id": payload.execution_id,
            "workflow_name": payload.workflow_name,
            "agent_name": payload.agent_name,
            "agent_type": payload.agent_type,
            "event_type": payload.event_type,
            "status": payload.status,
            "step_name": payload.step_name,
            "timestamp": payload.timestamp,
            "latency_ms": payload.latency_ms,
            "metadata": payload.metadata
        }
        telemetry_store.append(event_data)

        return {
            "success": True,
            "message": "Telemetry tracked",
            "session_id": payload.session_id,
            "event_count": len(telemetry_store)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/sessions/{session_id}")
def get_session_events(session_id: str):
    """Get all events for a session"""
    try:
        events = [e for e in telemetry_store if e["session_id"] == session_id]

        if not events:
            return {"error": "Session not found", "session_id": session_id}

        return {
            "session_id": session_id,
            "event_count": len(events),
            "events": events
        }
    except Exception as e:
        return {"error": str(e)}

# -------------------------
# Serve Static Files
# -------------------------
static_dir = pathlib.Path(__file__).parent
try:
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
except Exception as e:
    print(f"Warning: Could not mount static files: {e}")
