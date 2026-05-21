# Render Deployment - Two Web Services

Deploy as separate backend and frontend services for better scalability.

## Architecture

```
Service 1: Backend (FastAPI)
├─ Port: 10000 (auto-assigned)
├─ Start: gunicorn main:app --workers 3 --bind 0.0.0.0:$PORT
├─ Database: SQLite or PostgreSQL
└─ Serves: /api/*, /health, /sessions/*, /workflows/*, /agents/*

Service 2: Frontend (Static Files)
├─ Port: 10001 (auto-assigned)
├─ Start: python -m http.server 8000 --bind 0.0.0.0
├─ Serves: index.html, test.html, dashboard.html
└─ API calls to: Backend service URL
```

## Step 1: Create Backend Service

### 1a. In Render Dashboard

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Fill in details:
   - **Name:** `telemetry-backend`
   - **Runtime:** `Python 3.9`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn main:app --workers 3 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
   - **Plan:** Free (or Starter for 24/7)

### 1b. Add Environment Variables

In the "Environment" section, add:
- **DATABASE_URL** = `sqlite:///./telemetry.db`
- **DEBUG** = `false`
- **PYTHONUNBUFFERED** = `1`

### 1c. Deploy

Click "Create Web Service" and wait 2-5 minutes.

**Note the URL:** `https://telemetry-backend-xxxxx.onrender.com`

## Step 2: Update Frontend for Backend URL

Edit `test.html` and `dashboard.html`:

Replace:
```javascript
const API_URL = window.location.origin;
```

With:
```javascript
const API_URL = 'https://telemetry-backend-xxxxx.onrender.com';
```

(Replace xxxxx with your actual backend service name)

Or keep it dynamic and let Render manage it via environment variables.

### Alternative: Use Environment Variable

Create a file `config.js`:
```javascript
const API_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:8000'
  : 'https://telemetry-backend-xxxxx.onrender.com';
```

Then include in HTML:
```html
<script src="config.js"></script>
```

## Step 3: Create Frontend Service

### 3a. Create `run_frontend.py`

```python
#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = int(os.getenv('PORT', 8000))
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("0.0.0.0", PORT), MyHTTPRequestHandler) as httpd:
        print(f"Frontend serving on http://0.0.0.0:{PORT}")
        print(f"Home:       http://localhost:{PORT}/")
        print(f"Testing:    http://localhost:{PORT}/test.html")
        print(f"Dashboard:  http://localhost:{PORT}/dashboard.html")
        httpd.serve_forever()
```

### 3b. In Render Dashboard

1. Click **"New +"** → **"Web Service"**
2. Connect same GitHub repository
3. Fill in details:
   - **Name:** `telemetry-frontend`
   - **Runtime:** `Python 3.9`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python run_frontend.py`
   - **Plan:** Free

### 3c. NO Environment Variables Needed

Frontend doesn't need config - it serves static files.

### 3d. Deploy

Click "Create Web Service"

**Note the URL:** `https://telemetry-frontend-xxxxx.onrender.com`

## Step 4: Update Frontend Code

Edit `index.html`, `test.html`, and `dashboard.html`:

### Option A: Hardcode Backend URL (Simple)

```javascript
// In test.html and dashboard.html
const BACKEND_URL = 'https://telemetry-backend-xxxxx.onrender.com';
const API_URL = BACKEND_URL;

// In index.html for status check
fetch(`${BACKEND_URL}/health`)
```

### Option B: Detect Environment (Better)

```javascript
// Detect if running on Render or localhost
const isProduction = window.location.hostname.includes('onrender.com');

const API_URL = isProduction 
  ? 'https://telemetry-backend-xxxxx.onrender.com'
  : 'http://localhost:8000';
```

### Option C: Use Window Variable (Best)

Create `<script>` tag in HTML:
```html
<script>
  window.API_URL = 'https://telemetry-backend-xxxxx.onrender.com';
</script>
```

Then use:
```javascript
const API_URL = window.API_URL;
```

## Step 5: Verify Everything Works

### Test URLs

**Frontend:** https://telemetry-frontend-xxxxx.onrender.com/
**Backend:** https://telemetry-backend-xxxxx.onrender.com/health

### Quick Test

1. Visit frontend home page
2. Check backend status shows ✓
3. Go to Testing page
4. Send test event
5. Go to Dashboard
6. See event appear ✓

## File Structure for Two Services

```
telemetry_sdk/
├── Backend files:
│   ├── main.py              ← FastAPI server
│   ├── requirements.txt      ← Dependencies
│   └── telemetry.db        ← Database
│
├── Frontend files:
│   ├── index.html          ← Home page (updated)
│   ├── test.html           ← Testing (updated with BACKEND_URL)
│   ├── dashboard.html      ← Dashboard (updated with BACKEND_URL)
│   └── run_frontend.py     ← Frontend server (NEW)
│
└── Config files:
    ├── render.yaml         ← Not used (manual config)
    ├── .env               ← Local only
    ├── .env.example       ← Template
    └── requirements.txt   ← All dependencies
```

## Example: Updated test.html

Add this near the top of the `<script>` section:

```javascript
<script>
  // Configure backend URL
  const BACKEND_URL = 'https://telemetry-backend-xxxxx.onrender.com';
  const API_URL = BACKEND_URL;
  
  // ... rest of your code uses API_URL as before
</script>
```

## Example: Updated dashboard.html

Same approach:

```javascript
<script>
  const BACKEND_URL = 'https://telemetry-backend-xxxxx.onrender.com';
  const API_URL = BACKEND_URL;
  
  // ... rest of code unchanged
</script>
```

## Example: Updated index.html

For the health check:

```javascript
<script>
  const BACKEND_URL = 'https://telemetry-backend-xxxxx.onrender.com';
  
  async function checkBackend() {
    try {
      const response = await fetch(`${BACKEND_URL}/health`);
      // ... rest of function
    }
  }
</script>
```

## Environment Variables (Per Service)

### Backend Service (`telemetry-backend`)

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `sqlite:///./telemetry.db` |
| `DEBUG` | `false` |
| `PYTHONUNBUFFERED` | `1` |

### Frontend Service (`telemetry-frontend`)

No environment variables needed - serves static files only.

## Optional: Use Render Environment Variables

For dynamic configuration, use Render's environment variables:

### Backend Service

```ini
DATABASE_URL=sqlite:///./telemetry.db
DEBUG=false
PYTHONUNBUFFERED=1
BACKEND_URL=https://telemetry-backend-xxxxx.onrender.com
```

### Frontend Service

Create `.env` during build:
```bash
# In build command
echo "BACKEND_URL=https://telemetry-backend-xxxxx.onrender.com" > .env
```

## Advantages of Two Services

✅ **Independent Scaling**
- Scale backend if API calls increase
- Scale frontend if traffic increases

✅ **Separate Concerns**
- Backend: API and database
- Frontend: Static files and UI

✅ **Easy Updates**
- Update backend without rebuilding frontend
- Update UI without restarting API

✅ **Better Performance**
- Frontend can be cached/CDN-served
- Backend can use more resources

✅ **Flexibility**
- Use different runtimes if needed
- Deploy independently

## Cost Estimate

- **Backend Service (Free):** $0
- **Frontend Service (Free):** $0
- **Total:** $0 (can upgrade to Starter at $7/mo each)

For 24/7 uptime:
- **Backend (Starter):** $7/mo
- **Frontend (Starter):** $7/mo
- **Total:** $14/mo

## Monitoring

In Render Dashboard:

1. **Backend Service**
   - Monitor API metrics
   - Check database connections
   - Watch for errors

2. **Frontend Service**
   - Monitor traffic
   - Check response times
   - Verify assets loading

## Troubleshooting

### CORS Errors

**Problem:** Frontend can't call backend API
**Solution:** Add CORS headers in `run_frontend.py` or ensure backend has CORS enabled

```python
# In main.py, verify:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 502 Errors

**Backend:** Service still starting - wait 2-3 minutes
**Frontend:** Python server crashed - check logs

### Static Files 404

**Frontend:** Files not in root directory
**Solution:** Ensure index.html, test.html, dashboard.html in project root

### API Returns 404

**Backend:** Endpoint doesn't exist
**Solution:** Check API_REFERENCE.md for correct endpoints

## Complete Checklist

- [ ] Create Backend service (telemetry-backend)
- [ ] Note backend URL (e.g., https://telemetry-backend-xxxxx.onrender.com)
- [ ] Add environment variables to backend
- [ ] Backend deploys successfully
- [ ] Create Frontend service (telemetry-frontend)
- [ ] Update test.html with BACKEND_URL
- [ ] Update dashboard.html with BACKEND_URL
- [ ] Update index.html with BACKEND_URL
- [ ] Create run_frontend.py
- [ ] Frontend deploys successfully
- [ ] Test home page loads
- [ ] Test backend health check returns ✓
- [ ] Test sending event from Testing page
- [ ] Test Dashboard displays event
- [ ] All 3 pages work without errors

## Next Steps

1. Create Backend service first (following steps 1-3)
2. Note the backend URL
3. Update HTML files with backend URL
4. Create Frontend service (following steps 3-5)
5. Test everything

**Result:** Professional two-service deployment on Render! 🚀
