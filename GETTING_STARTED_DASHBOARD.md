# Getting Started with Telemetry Dashboard

Complete setup guide to get the dashboard running in 5 minutes.

## Prerequisites

- Python 3.7+
- FastAPI running on port 8000
- Modern web browser

## Quick Setup (5 minutes)

### Step 1: Install Dependencies (if not done yet)

```bash
pip install -r requirements.txt
```

### Step 2: Terminal 1 - Start FastAPI Backend

```bash
uvicorn main:app --reload
```

Wait for:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 3: Terminal 2 - Start Dashboard

#### Option A: Quick Launch (Recommended)

```bash
python run_dashboard.py
```

Dashboard automatically opens in your browser!

#### Option B: Manual Web Server

```bash
python -m http.server 8001
```

Then open in browser:
```
http://localhost:8001/dashboard.html
```

#### Option C: Direct Browser Open

Simply double-click `dashboard.html` in file explorer.

---

## ✓ You're Ready!

Your dashboard is now:
- ✅ Connected to FastAPI backend
- ✅ Auto-updating every 2 seconds
- ✅ Ready to receive telemetry

## First Test

### Test 1: Send Single Event

1. In dashboard, click **"Send Telemetry"**
2. Watch the dashboard update:
   - ✓ Metrics increase
   - ✓ Session appears
   - ✓ Event shows in timeline

### Test 2: Run Multi-Agent Demo

1. Click **"Run Demo (4 Agents)"**
2. Watch all 4 agents send telemetry
3. See complete workflow:
   - Salesforce → Boomi → D365 → M365
   - Total: 1000ms end-to-end
   - Success rate: 100%

### Test 3: Create Custom Workflow

1. Change Session ID: `my_workflow_001`
2. Send 3 events with different agents:
   - Event 1: Salesforce (status: success, latency: 200)
   - Event 2: Boomi (status: success, latency: 300)
   - Event 3: D365 (status: success, latency: 400)
3. Watch timeline show all 3 steps

---

## Dashboard Overview

```
┌─ Metrics (Top Left)
│  ├─ Total Sessions
│  ├─ Total Events
│  ├─ Success Rate
│  └─ Average Latency
│
├─ Sessions (Top Right)
│  └─ List all sessions with event counts
│
├─ Test Form (Middle Full Width)
│  ├─ Send single telemetry
│  ├─ Run multi-agent demo
│  └─ Clear dashboard
│
├─ Session Details (Bottom Left)
│  └─ Agent breakdown for selected session
│
├─ Timeline (Bottom Left)
│  └─ Visual flow of events
│
└─ Recent Events (Bottom Right)
   └─ Last 10 events with details
```

---

## Key Features

### 🔄 Auto-Refresh
- Dashboard updates every 2 seconds
- Toggle on/off with "Auto Refresh" switch
- Smooth animations while updating

### 📊 Real-Time Metrics
- Sessions count
- Total events
- Success rate percentage
- Average processing time

### 📋 Session Details
- Shows all agents in session
- Event counts per agent
- Success/error breakdown
- Total latency per agent

### ⏱️ Timeline View
- Visual event flow
- Numbered steps
- Status indicators (✓ ✕ ⏳)
- Timestamps

### 🧪 Test Form
- Quick telemetry sending
- Multiple agent types
- Custom values
- Instant feedback

---

## Common Workflows

### Lead to Order (4 Agents)

```bash
# Click "Run Demo (4 Agents)"
# OR manually:

Session: lead_to_order_001

1. Salesforce Agent (CRM)
   Event: Lead Detection
   Status: success
   Latency: 150ms

2. Boomi Agent (Integration)
   Event: Data Transform
   Status: success
   Latency: 280ms

3. D365 Agent (ERP)
   Event: Order Creation
   Status: success
   Latency: 450ms

4. M365 Agent (SaaS)
   Event: Notification
   Status: success
   Latency: 120ms

Total: 1000ms
Success: 100%
```

### Support Ticket Resolution (Custom)

```
Session: support_ticket_001

1. Ticket Received (Salesforce)
   Status: success
   Latency: 100ms

2. AI Analysis (Boomi)
   Status: success
   Latency: 500ms

3. Agent Assignment (D365)
   Status: success
   Latency: 200ms

4. Customer Notification (M365)
   Status: success
   Latency: 50ms

Total: 850ms
Success: 100%
```

---

## Troubleshooting

### Issue: "Cannot GET /dashboard.html"

**Solution:**
1. Make sure you're running `python -m http.server 8001` from the right directory
2. Dashboard file should be in same directory as this file
3. Access via `http://localhost:8001/dashboard.html`

### Issue: Dashboard won't update

**Solution:**
1. Check FastAPI is running: `http://127.0.0.1:8000/health`
2. Check browser console (F12) for errors
3. Toggle "Auto Refresh" off and on
4. Refresh browser (Ctrl+R)

### Issue: "Connection refused" error

**Solution:**
1. Ensure FastAPI is running on port 8000
2. Check firewall isn't blocking port 8000
3. Try accessing `http://127.0.0.1:8000/health` directly in browser

### Issue: Events not appearing after sending

**Solution:**
1. Check browser console for errors (F12)
2. Check FastAPI logs for errors
3. Try "Run Demo" first to verify setup
4. Check browser auto-refresh is enabled

---

## Architecture

```
Browser (Dashboard)
    ↓ JavaScript Fetch API
http://localhost:8001/dashboard.html
    ↓ Every 2 seconds
http://127.0.0.1:8000/workflows/...
    ↓
FastAPI Backend (main.py)
    ↓
SQLite Database (telemetry.db)
```

### Data Flow

```
1. Dashboard loads
   ↓
2. JavaScript starts
   ↓
3. Every 2 seconds:
   - Fetch /workflows/Lead-to-Order
   - Fetch /sessions/{session_id}/analytics
   - Update metrics
   - Update events
   - Render UI
   ↓
4. User sends telemetry via form
   ↓
5. POST /api/v1/telemetry
   ↓
6. FastAPI stores in database
   ↓
7. Next refresh cycle shows new data
```

---

## Next Steps

### Customize Dashboard
Edit `dashboard.html` to customize:
- Colors and styling
- Refresh interval
- Display fields
- Form fields

### Integration
Connect real agents to send telemetry:
- Salesforce Agentforce
- Boomi Integration
- Dynamics 365
- Microsoft 365

### Production
For production use:
- Enable authentication
- Use PostgreSQL instead of SQLite
- Add data retention policies
- Set up monitoring/alerts
- Deploy behind proxy

---

## File Structure

```
telemetry_sdk/
├── main.py                          # FastAPI backend
├── dashboard.html                   # Dashboard UI
├── run_dashboard.py                 # Launcher script
├── test_api.py                      # API tests
├── demo_multi_agent_session.py      # Multi-agent demo
├── requirements.txt                 # Dependencies
├── telemetry.db                     # SQLite database
├── README.md                        # API documentation
├── QUICKSTART.md                    # Quick start
├── API_REFERENCE.md                 # Complete API docs
├── MULTI_AGENT_GUIDE.md             # Multi-agent guide
├── DASHBOARD_SETUP.md               # Dashboard setup
└── GETTING_STARTED_DASHBOARD.md     # This file
```

---

## Quick Commands Reference

```bash
# Start FastAPI backend
uvicorn main:app --reload

# Start dashboard web server
python -m http.server 8001

# Or use launcher (auto-opens browser)
python run_dashboard.py

# Run multi-agent demo
python demo_multi_agent_session.py

# Test API
python test_api.py

# Query database
sqlite3 telemetry.db "SELECT * FROM telemetry_logs LIMIT 10;"
```

---

## Support

### FastAPI Issues
- Check logs: `uvicorn main:app --reload`
- Verify port 8000: `curl http://127.0.0.1:8000/health`
- Check CORS is enabled in main.py

### Dashboard Issues
- Open browser console: F12
- Check network tab for failed requests
- Verify FastAPI is accessible
- Try refreshing page

### Database Issues
- Check telemetry.db exists
- Verify permissions to write to directory
- Try deleting telemetry.db to reset (server will recreate)

---

**You're all set! Open the dashboard and start testing! 🚀**
