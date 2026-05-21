# Deployment Guide

## System Architecture

```
┌─────────────────────────────────────────────────┐
│         Client Browser (localhost:8001)         │
├──────────────────────────────────────────────────┤
│  Home (index.html)                              │
│  ├─ 🧪 Testing Page (test.html)                │
│  └─ 📊 Dashboard (dashboard.html)              │
├──────────────────────────────────────────────────┤
│         Python HTTP Server (port 8001)          │
│         Serves static HTML files                │
└─────────────────────────┬───────────────────────┘
                          │
                          │ CORS Requests
                          │
┌─────────────────────────▼───────────────────────┐
│    FastAPI Backend (localhost:8000)             │
├──────────────────────────────────────────────────┤
│  ✓ /api/v1/telemetry                           │
│  ✓ /sessions/{session_id}                      │
│  ✓ /workflows/{workflow_name}                  │
└─────────────────────────┬───────────────────────┘
                          │
                          │ SQL Queries
                          │
┌─────────────────────────▼───────────────────────┐
│     SQLite Database (telemetry.db)              │
└──────────────────────────────────────────────────┘
```

---

## File Structure

```
telemetry_sdk/
├── Backend Files
│   ├── main.py                    # FastAPI application
│   ├── requirements.txt            # Python dependencies
│   └── telemetry.db               # SQLite database
│
├── Frontend Files
│   ├── index.html                 # Landing page (HOME)
│   ├── test.html                  # Testing interface
│   └── dashboard.html             # Monitoring dashboard
│
├── Scripts & Config
│   ├── run_dashboard.py           # Web server launcher
│   ├── test_api.py                # API tests
│   └── demo_multi_agent_session.py # Demo script
│
└── Documentation
    ├── README.md                  # API overview
    ├── API_REFERENCE.md           # Complete API docs
    ├── GETTING_STARTED_DASHBOARD.md
    ├── DASHBOARD_SETUP.md
    ├── MULTI_AGENT_GUIDE.md
    ├── README_DASHBOARD.md
    ├── HOSTING.md                 # This file
    └── DEPLOYMENT.md              # Deployment guide
```

---

## Local Development (Recommended for Testing)

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
cd telemetry_sdk
pip install -r requirements.txt
```

### Step 2: Terminal 1 - Start Backend

```bash
uvicorn main:app --reload
```

Output should show:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Step 3: Terminal 2 - Start Web Server

```bash
python run_dashboard.py
```

This will:
1. Start web server on `http://localhost:8001`
2. Open your browser automatically
3. Display all available URLs

---

## Access the System

| Page | URL | Use Case |
|------|-----|----------|
| Landing | `http://localhost:8001/` | Start here - see all options |
| Testing | `http://localhost:8001/test.html` | Send test telemetry events |
| Dashboard | `http://localhost:8001/dashboard.html` | Monitor workflows in real-time |

---

## Production Deployment

### Option 1: Docker (Recommended)

**Step 1: Create Dockerfile**

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .
COPY *.html ./

# Expose ports
EXPOSE 8000 8001

# Start both services
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & python -m http.server 8001 --bind 0.0.0.0"]
```

**Step 2: Build and Run**

```bash
# Build
docker build -t telemetry-system:latest .

# Run
docker run -p 8000:8000 -p 8001:8001 -v telemetry_db:/app telemetry-system:latest
```

**Step 3: Deploy to Docker Hub or Cloud Registry**

```bash
# Tag for Docker Hub
docker tag telemetry-system:latest yourname/telemetry-system:latest

# Push
docker push yourname/telemetry-system:latest
```

---

### Option 2: Linux Server (Bare Metal)

**Step 1: SSH to Server**

```bash
ssh user@your-server.com
```

**Step 2: Clone/Upload Files**

```bash
cd /var/www
git clone <your-repo> telemetry-system
cd telemetry-system
```

Or upload manually:
```bash
scp -r telemetry_sdk/* user@server:/var/www/telemetry-system/
```

**Step 3: Install Python & Dependencies**

```bash
sudo apt update
sudo apt install python3 python3-pip
pip install -r requirements.txt
```

**Step 4: Create Systemd Service**

Create `/etc/systemd/system/telemetry-backend.service`:
```ini
[Unit]
Description=Telemetry FastAPI Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/telemetry-system
Environment="PATH=/usr/local/bin:/usr/bin"
ExecStart=/usr/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

Create `/etc/systemd/system/telemetry-web.service`:
```ini
[Unit]
Description=Telemetry Web Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/telemetry-system
ExecStart=/usr/bin/python3 -m http.server 8001 --bind 0.0.0.0
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

**Step 5: Enable and Start Services**

```bash
sudo systemctl daemon-reload
sudo systemctl enable telemetry-backend telemetry-web
sudo systemctl start telemetry-backend telemetry-web

# Check status
sudo systemctl status telemetry-backend
sudo systemctl status telemetry-web
```

**Step 6: Setup Nginx Reverse Proxy**

Create `/etc/nginx/sites-available/telemetry`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # Frontend - served by Python HTTP server
    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API - served by FastAPI
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /sessions/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }

    location /workflows/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }

    location /agents/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }

    location /health {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/telemetry /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

### Option 3: Cloud Platforms

#### AWS EC2

1. Launch Ubuntu 20.04 instance
2. Follow "Linux Server" steps above
3. Use AWS Certificate Manager for SSL
4. Setup CloudWatch monitoring

#### Google Cloud Run

```bash
gcloud run deploy telemetry-system \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8001
```

#### Azure App Service

```bash
az webapp up --name telemetry-system --runtime PYTHON:3.9
```

#### Heroku

1. Create `Procfile`:
```
web: python run_dashboard.py &
web: uvicorn main:app --port $PORT --host 0.0.0.0
```

2. Deploy:
```bash
heroku create telemetry-system
git push heroku main
```

---

## SSL/HTTPS Setup

### Using Let's Encrypt (Free)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

Auto-renewal:
```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

## Environment Configuration

Create `.env` file:
```env
# Database
DATABASE_URL=sqlite:///telemetry.db
# DATABASE_URL=postgresql://user:pass@localhost/telemetry

# API
API_HOST=0.0.0.0
API_PORT=8000

# Web
WEB_HOST=0.0.0.0
WEB_PORT=8001

# CORS
CORS_ORIGINS=["https://your-domain.com"]

# Debug
DEBUG=false
LOG_LEVEL=info
```

Load in `main.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///telemetry.db")
```

---

## Database Configuration

### PostgreSQL (Production Recommended)

Install:
```bash
sudo apt install postgresql postgresql-contrib
```

Create database:
```bash
sudo -u postgres psql
CREATE DATABASE telemetry;
CREATE USER telemetry_user WITH PASSWORD 'strong_password';
GRANT ALL PRIVILEGES ON DATABASE telemetry TO telemetry_user;
```

Update `.env`:
```env
DATABASE_URL=postgresql://telemetry_user:strong_password@localhost/telemetry
```

---

## Monitoring & Logs

### View Logs

```bash
# Backend logs
journalctl -u telemetry-backend -f

# Web server logs
journalctl -u telemetry-web -f

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Health Check

```bash
curl https://your-domain.com/health
```

### Database Status

```bash
sqlite3 telemetry.db "SELECT COUNT(*) as total_events FROM telemetry_logs;"
```

---

## Backup & Recovery

### Daily Backup

Create `/usr/local/bin/backup-telemetry.sh`:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp /var/www/telemetry-system/telemetry.db /backups/telemetry_$DATE.db
# Keep only last 30 days
find /backups -name "telemetry_*.db" -mtime +30 -delete
```

Make executable and add to crontab:
```bash
chmod +x /usr/local/bin/backup-telemetry.sh
echo "0 2 * * * /usr/local/bin/backup-telemetry.sh" | sudo crontab -
```

### Restore Backup

```bash
cp /backups/telemetry_20240101_020000.db /var/www/telemetry-system/telemetry.db
sudo systemctl restart telemetry-backend
```

---

## Performance Tuning

### FastAPI

Use Gunicorn for production:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 --timeout 120 main:app
```

### Database

Add indexes to frequently queried columns:
```python
# In main.py after creating tables
from sqlalchemy import Index
Index('idx_session_id', TelemetryLog.session_id).create(engine)
Index('idx_workflow_name', TelemetryLog.workflow_name).create(engine)
```

### Frontend

Update dashboard refresh interval (less frequent for production):
```javascript
// In dashboard.html, change:
refreshInterval = setInterval(updateDashboard, 5000); // 5 seconds instead of 2
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find process
lsof -i :8000
lsof -i :8001

# Kill process
kill -9 <PID>
```

### CORS Errors

1. Check frontend API_URL matches backend host
2. Verify CORS is enabled in main.py
3. Check browser console for error details

### Database Locked

```bash
# Delete lock file
rm telemetry.db-journal

# Restart service
sudo systemctl restart telemetry-backend
```

### Memory Issues

Monitor memory usage:
```bash
free -h
ps aux | grep python
```

Increase limits in systemd service:
```ini
MemoryLimit=2G
MemoryMax=3G
```

---

## Scaling

### Load Balancing

Use Nginx to load balance multiple backend instances:

```nginx
upstream telemetry_backends {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 443;
    server_name your-domain.com;

    location /api/ {
        proxy_pass http://telemetry_backends;
    }
}
```

### Database Replication

For PostgreSQL:
- Setup primary-replica replication
- Use replicas for read-heavy queries
- Configure failover with pg_basebackup

### Caching

Add Redis for caching:
```python
pip install redis
from redis import Redis

redis_client = Redis(host='localhost', port=6379)
```

---

## Security Checklist

- [ ] HTTPS enabled
- [ ] Firewall configured (only 80, 443 open)
- [ ] Database credentials in environment variables
- [ ] Regular backups automated
- [ ] Update log monitoring enabled
- [ ] Rate limiting configured
- [ ] CORS origins whitelisted
- [ ] SQL injection prevention (using SQLAlchemy ORM)
- [ ] Password hashing for any auth endpoints
- [ ] Regular dependency updates

---

## Getting Help

Check logs first:
```bash
journalctl -u telemetry-backend -n 50
```

Test connectivity:
```bash
curl -v https://your-domain.com/health
```

Check database:
```bash
sqlite3 telemetry.db "PRAGMA integrity_check;"
```

