# Dashboard Setup Guide

Complete guide to using the real-time telemetry dashboard.

## Quick Start

### Step 1: Start the FastAPI Backend

```bash
uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 2: Open the Dashboard

Simply open the `dashboard.html` file in your browser:

**Option A: Direct File Open**
```
File → Open → dashboard.html
```

Or in your file explorer, double-click `dashboard.html`

**Option B: Using Python Server (Recommended)**
```bash
# In a new terminal
python -m http.server 8001
```

Then open: `http://localhost:8001/dashboard.html`

## Dashboard Features

### 📈 Metrics Panel
Shows real-time metrics:
- **Sessions**: Total number of active sessions
- **Total Events**: All telemetry events collected
- **Success Rate**: Percentage of successful events
- **Avg Latency**: Average event processing time

### 🔗 Sessions List
- View all sessions
- Click on a session to see detailed breakdown
- See event count, agent count, and success rates per session
- Auto-updates every 2 seconds

### 🧪 Test Telemetry Form
Send test events directly from the dashboard:
- **Session ID**: Group events together (same workflow)
- **Agent Name**: Select from Salesforce, Boomi, D365, M365, or Custom
- **Workflow**: Name of the workflow (e.g., "Lead-to-Order")
- **Latency**: Simulated processing time in milliseconds
- **Status**: Success, Error, or Running
- **Event Type**: Agent Started, Completed, or Failed

### 📋 Session Details
Shows agent breakdown for selected session:
- Agent name and type
- Event counts
- Success/error counts
- Total latency for that agent
- Detailed workflow metrics

### ⏱️ Event Timeline
Visual timeline showing:
- Order of events in workflow
- Status of each event (✓ success, ✕ error, ⏳ running)
- Processing time for each step
- Timestamp of each event

### 📝 Recent Events
Last 10 events in reverse chronological order:
- Agent name
- Event type and status
- Processing latency
- Event timestamp

### ⚙️ Auto Refresh
Toggle automatic dashboard updates:
- **Enabled** (default): Dashboard refreshes every 2 seconds
- **Disabled**: Manual refresh only (refresh browser to update)

## How to Use

### Scenario 1: Send Single Event

1. Fill in the Test Telemetry form:
   - Session ID: `mytest_001`
   - Agent: `Salesforce Agent`
   - Status: `success`
   - Latency: `200`

2. Click **Send Telemetry**

3. Watch the dashboard update:
   - Metrics change
   - Session appears in Sessions list
   - Event appears in Recent Events
   - Timeline updates

### Scenario 2: Multi-Agent Workflow

1. Click **Run Demo (4 Agents)**

2. Dashboard automatically sends telemetry from:
   - Salesforce Agent (150ms)
   - Boomi Agent (280ms)
   - D365 Agent (450ms)
   - M365 Agent (120ms)

3. All events linked with same session_id

4. View results:
   - Metrics show 4 events, 100% success, 1000ms total
   - Click session to see agent breakdown
   - Timeline shows all 4 steps in order
   - Session details shows each agent's contribution

### Scenario 3: Custom Agents

1. Create your own agents:
   - Change **Agent Name** to custom name
   - Change **Agent Type** in form
   - Send telemetry from multiple agents with same session ID

2. Dashboard automatically:
   - Creates new session
   - Tracks all agents
   - Calculates metrics
   - Shows timeline

## Real-Time Updates

The dashboard updates automatically every 2 seconds:

```
Refresh Cycle (2s interval):
1. Fetch all workflows
2. Fetch session analytics for each
3. Update metrics
4. Update sessions list
5. Update events and timeline
6. Render UI
```

No manual refresh needed!

## Dashboard Architecture

```
Browser Dashboard (dashboard.html)
        ↓
    JavaScript
        ↓
    Fetch API
        ↓
    FastAPI Backend (main.py)
        ↓
    SQLite Database (telemetry.db)
```

### Data Flow

```
1. Send Telemetry
   Form → POST /api/v1/telemetry → SQLite

2. Fetch Data
   Dashboard → GET /workflows/{name} → SQLite

3. Display Data
   JSON → JavaScript → HTML → Browser

4. Auto Update
   Every 2s → Repeat step 2 & 3
```

## Testing Workflows

### Lead-to-Order (4 Agents)

Click "Run Demo" to automatically execute:

```
Salesforce (Lead Detection)
    ↓ 150ms
Boomi (Data Enrichment)
    ↓ 280ms
D365 (Order Creation)
    ↓ 450ms
M365 (Notification)
    ↓ 120ms
Total: 1000ms
```

### Custom Multi-Step Process

1. Session ID: `custom_workflow_001`
2. Send first event:
   - Agent: Custom Agent 1
   - Event: agent_started
   - Latency: 0
3. Send second event:
   - Agent: Custom Agent 2
   - Event: agent_completed
   - Latency: 500
4. Send third event:
   - Agent: Custom Agent 3
   - Event: agent_completed
   - Latency: 300

Dashboard shows complete 3-step workflow!

## Troubleshooting

### Dashboard shows "No sessions yet"

**Check:**
1. Is FastAPI backend running? 
   ```bash
   curl http://localhost:8000/health
   ```

2. Did you send telemetry?
   - Click "Send Telemetry" or "Run Demo"

3. Is auto-refresh enabled?
   - Toggle the "Auto Refresh" switch

### Metrics not updating

**Solution:**
1. Make sure auto-refresh is enabled
2. Check browser console (F12) for errors
3. Verify FastAPI is running and accessible
4. Try refreshing the page (Ctrl+R)

### Events not appearing

**Check:**
1. Is session_id correct?
   - Same session_id = linked events
   - Different session_id = separate sessions

2. Did the request succeed?
   - "Send Telemetry" button should show confirmation

3. Check FastAPI logs for errors

### "Failed to fetch" error

**Solution:**
1. Ensure FastAPI backend is running
2. Check CORS is enabled in main.py
3. Verify correct URL: `http://127.0.0.1:8000`
4. Check no firewall blocking port 8000

## Browser Requirements

- Modern browser (Chrome, Firefox, Safari, Edge)
- JavaScript enabled
- Supports Fetch API
- Supports CSS Grid and Flexbox

## Performance

Dashboard is optimized for:
- Fast updates (2-second refresh)
- Smooth animations
- Responsive design
- Works on desktop and tablet
- Mobile-friendly responsive layout

## Customization

Edit dashboard.html to customize:

### Change refresh interval
```javascript
// Line ~750: Change 2000 to your interval (milliseconds)
refreshInterval = setInterval(updateDashboard, 2000);
```

### Change colors
```css
/* Line ~80-90: Gradient colors */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Change displayed fields
```javascript
// Line ~500+: Update HTML generation
```

## Export Data

To export dashboard data:

1. Query API directly:
```bash
curl http://localhost:8000/sessions/session_id/analytics > session.json
```

2. Query database directly:
```bash
sqlite3 telemetry.db "SELECT * FROM telemetry_logs;" > export.csv
```

3. Build custom export from API endpoints

---

**Ready to test?** Open `dashboard.html` and click "Run Demo (4 Agents)"! 🚀
