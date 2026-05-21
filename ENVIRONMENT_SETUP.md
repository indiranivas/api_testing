# Environment Configuration Guide

Complete guide for setting up environment variables and configuration for all deployment scenarios.

## Local Development Setup

### 1. Create `.env` File

Copy the example file:
```bash
cp .env.example .env
```

### 2. Default Local Configuration

The `.env` file includes:

```env
# Local Development
DATABASE_URL=sqlite:///./telemetry.db
API_HOST=0.0.0.0
API_PORT=8000
WEB_HOST=0.0.0.0
WEB_PORT=8001
DEBUG=false
LOG_LEVEL=info
```

### 3. Run Locally

```bash
# Terminal 1: Backend
uvicorn main:app --reload

# Terminal 2: Web Server
python run_dashboard.py
```

Visit: `http://localhost:8001/`

## Production Deployment

### Environment Variables by Platform

#### Docker (Local Machine)

Create `.env` in project root:
```env
DATABASE_URL=sqlite:///./telemetry.db
DEBUG=false
PYTHONUNBUFFERED=1
```

Run:
```bash
docker build -t telemetry-system .
docker run -p 8000:8000 --env-file .env telemetry-system
```

#### Render.com

**No `.env` file needed!** Render uses `render.yaml`:

```yaml
envVars:
  - key: DATABASE_URL
    value: sqlite:///./telemetry.db
  - key: DEBUG
    value: "false"
  - key: PYTHONUNBUFFERED
    value: "1"
```

See `RENDER_SETUP.md` for complete instructions.

#### Linux Server (Systemd)

Create `/etc/telemetry/.env`:
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/telemetry
DEBUG=false
LOG_LEVEL=info
```

Update systemd service:
```ini
[Service]
EnvironmentFile=/etc/telemetry/.env
ExecStart=/usr/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

#### AWS / Azure / GCP

Use cloud platform's secrets management:

**AWS Secrets Manager:**
```bash
aws secretsmanager create-secret \
  --name telemetry/db-url \
  --secret-string "postgresql://..."
```

**Azure Key Vault:**
```bash
az keyvault secret set \
  --vault-name telemetry-kv \
  --name db-url \
  --value "postgresql://..."
```

**Google Cloud Secrets:**
```bash
echo -n "postgresql://..." | gcloud secrets create db-url
```

Then update code to read from secrets.

#### Heroku

Set environment variables:
```bash
heroku config:set DATABASE_URL=postgresql://...
heroku config:set DEBUG=false
```

Or in `Procfile`:
```
web: python run_dashboard.py &
    uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Database Configuration

### SQLite (Development)

```env
DATABASE_URL=sqlite:///./telemetry.db
```

- File-based database
- No setup required
- Best for: Local development, small deployments
- Limitations: Single connection, no concurrent access

### PostgreSQL (Production)

#### Local PostgreSQL

```bash
# Install
sudo apt install postgresql postgresql-contrib

# Create database
sudo -u postgres psql
CREATE DATABASE telemetry;
CREATE USER telemetry_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE telemetry TO telemetry_user;
```

```env
DATABASE_URL=postgresql://telemetry_user:secure_password@localhost:5432/telemetry
```

#### Remote PostgreSQL

Use cloud provider or managed service:

**Render Database:**
```env
DATABASE_URL=postgresql://user:pass@dpg-xxx.render.com:5432/telemetry
```

**AWS RDS:**
```env
DATABASE_URL=postgresql://admin:password@telemetry-db.xxxxx.us-east-1.rds.amazonaws.com:5432/telemetry
```

**Azure Database:**
```env
DATABASE_URL=postgresql://user@server:password@server.postgres.database.azure.com:5432/telemetry
```

## API Configuration

### CORS (Cross-Origin Resource Sharing)

Default (allows all origins):
```python
allow_origins=["*"]
```

For production, whitelist specific origins:

```env
CORS_ORIGINS=["https://yourdomain.com", "https://app.yourdomain.com"]
```

Update `main.py`:
```python
import json
from os import getenv

cors_origins = json.loads(getenv("CORS_ORIGINS", '["*"]'))
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Port Configuration

Local Development:
```env
API_PORT=8000
WEB_PORT=8001
```

Production (Render, Heroku, etc.):
- Platform assigns port via `$PORT` environment variable
- Application should read: `port = int(os.getenv("PORT", 8000))`

## Security Configuration

### Development vs Production

**Development:**
```env
DEBUG=true
PYTHONUNBUFFERED=1
CORS_ORIGINS=["*"]
DATABASE_URL=sqlite:///./telemetry.db
```

**Production:**
```env
DEBUG=false
CORS_ORIGINS=["https://yourdomain.com"]
DATABASE_URL=postgresql://secure_creds@host/db
LOG_LEVEL=warning
```

### Secrets Management

**Never commit sensitive data!**

Good practices:
```bash
✓ USE: Environment variables
✓ USE: Cloud secrets (AWS Secrets, Azure Key Vault)
✓ USE: .env files locally (add to .gitignore)
✗ DON'T: Hardcode passwords in code
✗ DON'T: Commit .env to Git
✗ DON'T: Use default credentials
```

### Render Secrets

Store sensitive data in Render dashboard:

1. Go to service settings
2. "Environment" tab
3. Add secret variables (these don't show in logs)

Example secrets:
- `DATABASE_URL` (if using external DB)
- `API_KEY` (if adding authentication)

## Logging Configuration

### Log Levels

```env
LOG_LEVEL=debug      # Verbose, all information
LOG_LEVEL=info       # Standard operation
LOG_LEVEL=warning    # Important but non-critical
LOG_LEVEL=error      # Errors only
```

### Log Files

For persistent logging:

```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Feature Flags

Enable/disable features via environment:

```env
DEBUG=true
ENABLE_METRICS=true
ENABLE_RATE_LIMITING=false
MAX_REQUESTS_PER_MINUTE=100
```

Update code:
```python
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
ENABLE_METRICS = os.getenv("ENABLE_METRICS", "true").lower() == "true"
MAX_REQUESTS = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "100"))
```

## Troubleshooting

### "No module named 'dotenv'"

```bash
pip install python-dotenv
```

### Environment variables not loading

Check:
1. Is `.env` file in project root? 
2. Does code call `load_dotenv()`?
3. Correct syntax: `KEY=value` (no spaces around `=`)

### Variables show as None

Check:
1. Variable is set in `.env`
2. Correct variable name
3. `.env` is not in `.gitignore` (for development)
4. Using `os.getenv("VAR_NAME")` correctly

### CORS errors in production

Add your domain to `CORS_ORIGINS`:
```env
CORS_ORIGINS=["https://yourdomain.com"]
```

### Database connection fails

For PostgreSQL:
```bash
# Test connection
psql postgresql://user:pass@host:5432/db

# Check credentials
echo $DATABASE_URL

# Check network access
telnet host 5432
```

## Reference

| Variable | Default | Purpose |
|----------|---------|---------|
| `DATABASE_URL` | `sqlite:///./telemetry.db` | Database connection string |
| `API_PORT` | `8000` | FastAPI server port |
| `WEB_PORT` | `8001` | Web server port |
| `DEBUG` | `false` | Debug mode (true/false) |
| `LOG_LEVEL` | `info` | Logging verbosity |
| `CORS_ORIGINS` | `["*"]` | Allowed origins (JSON array) |
| `PYTHONUNBUFFERED` | `1` | Unbuffered stdout (for logging) |

## Next Steps

1. **Local Development**: Use `.env` with SQLite
2. **Testing**: Push to GitHub
3. **Production**: Deploy to Render with `render.yaml`
4. **Monitoring**: Check logs in Render dashboard
5. **Scaling**: Upgrade plan or use PostgreSQL

See also:
- `RENDER_SETUP.md` - Render deployment
- `DEPLOYMENT.md` - Advanced deployment
- `START.md` - Quick start
