# Telemetry Dashboard - Complete System

Professional telemetry tracking system with real-time web dashboard for multi-agent workflow monitoring.

## 🎯 What You Have

### Backend API (FastAPI + SQLite)
- Multi-platform telemetry collection
- Session-based event linking
- Real-time analytics
- Cross-platform aggregation

### Frontend Dashboard (Modern Web UI)
- Real-time metrics display
- Live event tracking
- Session management
- Multi-agent workflow visualization
- Test telemetry sender
- Auto-refresh (every 2 seconds)

## 🚀 Start in 3 Steps

### Terminal 1: Start Backend
```bash
uvicorn main:app --reload
```

### Terminal 2: Start Dashboard
```bash
python run_dashboard.py
```

### Browser Opens Automatically
Dashboard available at `http://localhost:8001/dashboard.html`

---

## 📊 Dashboard Features

### Real-Time Metrics
```
┌─────────────────────┐
│ Sessions   Events   │
│    0        0      │
│ Success    Latency  │
│   0%       0ms     │
└─────────────────────┘
```

### Session Management
```
Sessions List:
├─ test_session_001
│  └─ 4 agents • 4 events • 100% success
├─ workflow_lead_to_order_001
│  └─ 4 agents • 4 events • 100% success
└─ custom_workflow_001
   └─ 3 agents • 3 events • 100% success
```

### Test Telemetry Form
```
┌─────────────────────────────────────┐
│ Session ID:    test_session_001    │
│ Agent Name:    Salesforce Agent    │
│ Workflow:      Lead-to-Order       │
│ Latency:       250  ms            │
│ Status:        Success            │
│ Event Type:    Agent Completed    │
├─────────────────────────────────────┤
│ [Send Telemetry] [Run Demo (4)] [Clear] │
└─────────────────────────────────────┘
```

### Event Timeline
```
Workflow Trace:

1. Salesforce Agent (CRM)
   Lead Detection - 150ms - ✓ success

2. Boomi Agent (Integration)
   Data Transform - 280ms - ✓ success

3. D365 Agent (ERP)
   Order Creation - 450ms - ✓ success

4. M365 Agent (SaaS)
   Notification - 120ms - ✓ success

Total: 1000ms | Success: 100%
```

---

## 🧪 Testing Features

### Instant Telemetry Sending
1. Fill form in dashboard
2. Click "Send Telemetry"
3. See dashboard update in real-time

### Multi-Agent Demo
1. Click "Run Demo (4 Agents)"
2. Automatically sends:
   - Salesforce telemetry (CRM)
   - Boomi telemetry (Integration)
   - D365 telemetry (ERP)
   - M365 telemetry (SaaS)
3. All linked with same session_id
4. Dashboard shows complete workflow

### Custom Workflows
Create any workflow:
1. Change session_id in form
2. Select different agents
3. Send multiple events
4. Dashboard tracks everything

---

## 📈 Real-Time Updates

Dashboard auto-refreshes every 2 seconds:

```
Loop:
  ├─ Fetch session data
  ├─ Calculate metrics
  ├─ Update UI
  └─ Repeat in 2 seconds
```

Toggle "Auto Refresh" to enable/disable.

---

## 🏗️ System Architecture

```
┌─────────────────┐
│   Web Browser   │
│   dashboard.html│
│   (Modern UI)   │
└────────┬────────┘
         │ Fetch API
         │ (Every 2s)
         ▼
┌─────────────────┐
│  FastAPI Server │
│  (main.py)      │
│  Port: 8000     │
└────────┬────────┘
         │ SQL
         │ Queries
         ▼
┌─────────────────┐
│ SQLite Database │
│ (telemetry.db)  │
└─────────────────┘
```

## 📁 Files

### Core Application
- **main.py** - FastAPI backend with all endpoints
- **dashboard.html** - Web dashboard UI
- **telemetry.db** - SQLite database (auto-created)

### Utilities
- **run_dashboard.py** - Launcher script
- **test_api.py** - API tests
- **demo_multi_agent_session.py** - Multi-agent demo

### Documentation
- **GETTING_STARTED_DASHBOARD.md** - Quick start (READ THIS FIRST)
- **DASHBOARD_SETUP.md** - Detailed dashboard guide
- **API_REFERENCE.md** - Complete API documentation
- **MULTI_AGENT_GUIDE.md** - Multi-agent tracking guide
- **README.md** - API overview
- **QUICKSTART.md** - Quick start (original)

## 🎨 Dashboard Design

Modern gradient UI with:
- Responsive layout (desktop, tablet, mobile)
- Real-time animations
- Smooth transitions
- Professional color scheme (purple gradient)
- Easy-to-read metrics
- Intuitive forms
- Visual timeline

## 🔄 Data Flow

### Sending Telemetry
```
Form Input
    ↓
POST /api/v1/telemetry
    ↓
FastAPI processes
    ↓
SQLite stores
    ↓
Dashboard fetches (next cycle)
    ↓
UI updates automatically
```

### Multiple Platforms
```
Salesforce Agent
    ↓
POST /api/v1/salesforce/telemetry
    ↓ ┐
   ├─┼─→ SQLite (Same Session ID)
   │ ↓
Boomi Agent
    ↓
POST /api/v1/boomi/telemetry
    ↓ ┐
   ├─┼─→ SQLite (Same Session ID)
   │ ↓
D365 Agent
    ↓
POST /api/v1/d365/telemetry
    ↓ ┐
   └─┼─→ SQLite (Same Session ID)
     ↓
Dashboard Queries
    ↓
Shows all agents linked!
```

## 🌟 Key Capabilities

✅ **Multi-Platform Collection**
- Salesforce Agentforce
- Boomi Integration
- Dynamics 365
- Microsoft 365
- Custom agents

✅ **Session Tracking**
- Automatic linking by session_id
- Complete workflow visibility
- Cross-platform correlation

✅ **Real-Time Updates**
- 2-second refresh cycle
- Smooth animations
- No manual refresh needed

✅ **Testing Tools**
- Instant telemetry sending
- Multi-agent demo
- Custom workflows
- Form validation

✅ **Analytics**
- Success rates
- Latency metrics
- Agent breakdown
- Workflow summaries

✅ **Professional UI**
- Modern design
- Responsive layout
- Real-time metrics
- Visual timeline

## 🚀 Quick Commands

```bash
# Start backend
uvicorn main:app --reload

# Start dashboard (auto-opens browser)
python run_dashboard.py

# Or manual server
python -m http.server 8001

# Run multi-agent demo
python demo_multi_agent_session.py

# Test API
python test_api.py

# Query database
sqlite3 telemetry.db "SELECT * FROM telemetry_logs;"
```

## 📊 Example Metrics

After running demo:

```
Metrics:
├─ Sessions: 1
├─ Total Events: 4
├─ Success Rate: 100%
└─ Avg Latency: 250ms

Session: test_session_001
├─ Event 1: Salesforce Agent (150ms) ✓
├─ Event 2: Boomi Agent (280ms) ✓
├─ Event 3: D365 Agent (450ms) ✓
└─ Event 4: M365 Agent (120ms) ✓

Total: 1000ms | Success: 100%
```

## 🎓 Learning Path

1. **Read**: GETTING_STARTED_DASHBOARD.md
2. **Run**: `python run_dashboard.py`
3. **Test**: Click "Run Demo (4 Agents)"
4. **Explore**: Send custom telemetry
5. **Understand**: Read MULTI_AGENT_GUIDE.md
6. **Integrate**: Connect real agents

## 🔧 Customization

### Colors
Edit `dashboard.html` line 80-90:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Refresh Interval
Edit `dashboard.html` line 750:
```javascript
refreshInterval = setInterval(updateDashboard, 2000); // 2 seconds
```

### Add Fields
Edit test form in `dashboard.html` to add custom fields.

## 🐛 Troubleshooting

**Dashboard won't load?**
- Ensure FastAPI is running
- Check port 8000 is accessible
- Check CORS is enabled in main.py

**Events not appearing?**
- Check browser console (F12) for errors
- Ensure auto-refresh is enabled
- Check FastAPI logs for errors

**Metrics not updating?**
- Toggle auto-refresh off/on
- Refresh browser (Ctrl+R)
- Check network tab in F12 for failed requests

## 📞 Support

### FastAPI Issues
```bash
curl http://127.0.0.1:8000/health
```

### Database Issues
```bash
sqlite3 telemetry.db ".tables"
```

### Dashboard Issues
- Open browser console (F12)
- Check Network tab for failed requests
- Check FastAPI logs

---

## 🎉 You're Ready!

**Everything is set up and ready to use!**

1. **Start the backend**:
   ```bash
   uvicorn main:app --reload
   ```

2. **Start the dashboard**:
   ```bash
   python run_dashboard.py
   ```

3. **Click "Run Demo (4 Agents)"** in dashboard

4. **Watch telemetry flow through all 4 platforms in real-time!**

---

**Questions?** Check the documentation files included in this directory.

**Want to integrate real agents?** See MULTI_AGENT_GUIDE.md

**Need API details?** See API_REFERENCE.md

Happy monitoring! 📊✨
