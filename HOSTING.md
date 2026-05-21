# Hosting the Telemetry System

## Quick Start (Local Development)

### Terminal 1: Start FastAPI Backend
```bash
uvicorn main:app --reload
```

Wait for:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Terminal 2: Start Web Server
```bash
python run_dashboard.py
```

This will:
- Start web server on `http://localhost:8001`
- Automatically open your browser to the home page
- Display all available URLs

---

## Access Points

Once running:

| Page | URL | Purpose |
|------|-----|---------|
| **Home** | `http://localhost:8001/` | Landing page with navigation |
| **Testing** | `http://localhost:8001/test.html` | Send test events |
| **Dashboard** | `http://localhost:8001/dashboard.html` | Monitor workflows |

---

## Production Hosting

### Option 1: Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy backend files
COPY main.py requirements.txt ./

# Install dependencies
RUN pip install -r requirements.txt

# Copy web files
COPY *.html ./

# Expose ports
EXPOSE 8000 8001

# Start FastAPI (production)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t telemetry-system .
docker run -p 8000:8000 -p 8001:8001 telemetry-system
```

### Option 2: Gunicorn + Nginx

**Start FastAPI with Gunicorn:**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

**Serve HTML with Nginx:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Static files
    location / {
        root /path/to/telemetry_sdk;
        try_files $uri $uri/ /index.html;
    }

    # API proxy
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /sessions/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }

    location /workflows/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }
}
```

### Option 3: Heroku

1. Create `Procfile`:
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT main:app
release: python -c "from sqlalchemy import create_engine; create_engine('sqlite:///telemetry.db')"
```

2. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

### Option 4: AWS/Azure/GCP

**Copy files to server:**
```bash
scp -r telemetry_sdk/* user@server:/var/www/telemetry/
```

**Install on server:**
```bash
cd /var/www/telemetry
pip install -r requirements.txt
```

**Start with systemd (Linux):**

Create `/etc/systemd/system/telemetry.service`:
```ini
[Unit]
Description=Telemetry System
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/var/www/telemetry
ExecStart=/usr/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable telemetry
sudo systemctl start telemetry
```

---

## Configuration

### Backend Settings (main.py)

Change database:
```python
# SQLite (default)
DATABASE_URL = "sqlite:///telemetry.db"

# PostgreSQL
DATABASE_URL = "postgresql://user:password@localhost/telemetry"

# MySQL
DATABASE_URL = "mysql+pymysql://user:password@localhost/telemetry"
```

### Frontend Settings

Edit `dashboard.html`:
```javascript
// Change API URL
const API_URL = 'http://your-domain.com:8000';
```

Edit `test.html`:
```javascript
// Change API URL
const API_URL = 'http://your-domain.com:8000';
```

---

## Environment Variables

Create `.env` file:
```
DATABASE_URL=sqlite:///telemetry.db
CORS_ORIGINS=["http://localhost:3000", "http://your-domain.com"]
API_HOST=0.0.0.0
API_PORT=8000
```

Load in `main.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Reverse Proxy Setup

### Using Apache

```apache
<VirtualHost *:80>
    ServerName your-domain.com

    # Static files
    DocumentRoot /var/www/telemetry
    <Directory /var/www/telemetry>
        Options Indexes FollowSymLinks
        AllowOverride All
    </Directory>

    # API proxy
    ProxyPreserveHost On
    ProxyPass /api http://127.0.0.1:8000/api
    ProxyPassReverse /api http://127.0.0.1:8000/api

    ProxyPass /sessions http://127.0.0.1:8000/sessions
    ProxyPassReverse /sessions http://127.0.0.1:8000/sessions

    ProxyPass /workflows http://127.0.0.1:8000/workflows
    ProxyPassReverse /workflows http://127.0.0.1:8000/workflows
</VirtualHost>
```

---

## Security

### Enable HTTPS

**Using Let's Encrypt (Certbot):**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### CORS Configuration

Update `main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Database Security

- Use PostgreSQL instead of SQLite for production
- Enable authentication on all endpoints
- Use environment variables for credentials
- Implement rate limiting

---

## Monitoring

### Health Check

```bash
curl http://127.0.0.1:8000/health
```

### Database Size

```bash
sqlite3 telemetry.db "SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size();"
```

### Logs

**FastAPI:**
```bash
# Run with logging
uvicorn main:app --log-level debug
```

**Systemd:**
```bash
journalctl -u telemetry -f
```

---

## Maintenance

### Backup Database

```bash
cp telemetry.db telemetry.db.backup
```

### Clear Old Data

```python
from sqlalchemy import delete
from main import TelemetryLog
from datetime import datetime, timedelta

# Delete events older than 30 days
cutoff = datetime.utcnow() - timedelta(days=30)
session.execute(delete(TelemetryLog).where(TelemetryLog.timestamp < cutoff))
session.commit()
```

### Update Dependencies

```bash
pip install -r requirements.txt --upgrade
```

---

## Troubleshooting

**Port already in use:**
```bash
# Find process using port 8001
lsof -i :8001

# Kill process
kill -9 <PID>
```

**Database locked:**
```bash
# Check if server is running
ps aux | grep python

# Delete lock file
rm telemetry.db-journal
```

**CORS errors:**
- Ensure backend is running on port 8000
- Check CORS_ORIGINS in `.env`
- Verify frontend API_URL matches backend host

---

## Support

For issues, check:
1. FastAPI logs: `uvicorn main:app --reload`
2. Browser console: `F12` → Console tab
3. Network tab: `F12` → Network tab
4. Database: `sqlite3 telemetry.db ".tables"`

