# Deploy to Render

Complete guide for deploying the telemetry system to Render.com

## Prerequisites

- GitHub account with your repository
- Render.com account (free tier available)
- Repository pushed to GitHub

## Step 1: Prepare Your Repository

The system includes a `render.yaml` configuration file. Make sure these files are in your repo:

```
telemetry_sdk/
├── main.py
├── requirements.txt
├── render.yaml          ← Required
├── .env                 ← Not committed (in .gitignore)
├── index.html
├── test.html
├── dashboard.html
└── ... (other files)
```

## Step 2: Connect GitHub to Render

1. Go to **https://dashboard.render.com**
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect Account"** and authorize GitHub
4. Select your repository
5. Click **"Connect"**

## Step 3: Configure Service (Render auto-detects render.yaml)

Render will automatically detect `render.yaml` and use these settings:

| Setting | Value |
|---------|-------|
| **Name** | telemetry-system |
| **Runtime** | Python 3.9 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn main:app --workers 3 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT` |
| **Plan** | Free (or paid if needed) |

## Step 4: Environment Variables

Render automatically sets these from `render.yaml`:

```
DATABASE_URL = sqlite:///./telemetry.db
DEBUG = false
PYTHONUNBUFFERED = 1
```

**For PostgreSQL (Production):**

If you want to use PostgreSQL instead:

1. In Render dashboard, click your service
2. Go to **"Environment"** tab
3. Change `DATABASE_URL` to:
   ```
   postgresql://user:password@your-db:5432/telemetry
   ```
4. Redeploy

## Step 5: Deploy

1. Click **"Create Web Service"**
2. Render will build and deploy automatically
3. Watch the logs in the "Logs" tab
4. Once deployed, you'll get a URL like: `https://telemetry-system.onrender.com`

## Step 6: Access Your System

Once deployed:

| Page | URL |
|------|-----|
| **Home** | `https://telemetry-system.onrender.com/` |
| **Testing** | `https://telemetry-system.onrender.com/test.html` |
| **Dashboard** | `https://telemetry-system.onrender.com/dashboard.html` |
| **API** | `https://telemetry-system.onrender.com/api/v1/telemetry` |

## How It Works

1. **Gunicorn** serves the FastAPI app on port 8000
2. **FastAPI** mounts static files (HTML) at root path `/`
3. All requests are routed through a single port
4. Database uses SQLite (auto-created on first run)

```
┌─────────────────────────────────────────┐
│  Render.com (HTTPS)                     │
│  https://telemetry-system.onrender.com  │
├─────────────────────────────────────────┤
│  Gunicorn + Uvicorn Workers             │
│  (FastAPI + Static Files)               │
├─────────────────────────────────────────┤
│  SQLite Database (telemetry.db)         │
└─────────────────────────────────────────┘
```

## Monitoring & Logs

In Render dashboard:

1. Click your service
2. Go to **"Logs"** tab to see real-time logs
3. Watch for errors during startup

Common log entries:
```
INFO: Application startup complete
INFO: Uvicorn running on http://0.0.0.0:10000
```

## Testing After Deployment

1. Visit `https://telemetry-system.onrender.com/`
2. Check if backend status shows "Backend is running ✓"
3. Go to **Testing** page
4. Send a test event
5. Go to **Dashboard** and verify data appears

## Troubleshooting

### Build Fails
- Check `requirements.txt` is valid
- Verify `render.yaml` syntax
- Look at "Logs" tab for specific errors

### 502 Bad Gateway
- Service might still be starting
- Check logs for startup errors
- Service might have run out of memory (upgrade plan)

### Database Errors
```
Error: unable to open database file
```
- SQLite database doesn't persist on Render's file system
- Consider upgrading to PostgreSQL
- Or use a connected PostgreSQL database

### Static Files Not Loading
- Check main.py has StaticFiles mounting code
- Verify HTML files are in root directory
- Check file permissions

## Production Recommendations

### 1. Use PostgreSQL Instead of SQLite

Create a PostgreSQL database on Render:

1. In Render, click **"New +"** → **"PostgreSQL"**
2. Create database
3. Copy connection string
4. Update environment variable in web service

### 2. Enable HTTPS (Auto)

Render automatically provides HTTPS for all domains

### 3. Setup Auto-Deploys

1. Go to service settings
2. Enable **"Auto-Deploy"** from main branch
3. Every push to GitHub will auto-deploy

### 4. Monitor Performance

1. Go to **"Metrics"** tab
2. Watch CPU, Memory, Network usage
3. Upgrade plan if needed

### 5. Setup Backups

For SQLite:
- Download database periodically using Render's shell
- Or migrate to PostgreSQL with built-in backups

For PostgreSQL:
- Render provides automatic backups
- Accessible in database dashboard

## Update & Redeploy

To update your code:

```bash
# Make changes
git add .
git commit -m "Update telemetry system"

# Push to GitHub
git push origin main

# Render auto-deploys (if enabled)
# Or manually redeploy:
# 1. Go to Render dashboard
# 2. Click service
# 3. Click "Manual Deploy" button
```

## Cost

- **Free Plan**
  - 1 web service
  - 750 hours/month
  - 0.5 GB memory
  - No custom domain
  - Shuts down after 15 min inactivity

- **Starter Plan** ($7/month)
  - Keeps service running 24/7
  - Custom domain support
  - Auto-deploy
  - Better performance

- **PostgreSQL** ($7-15/month)
  - 5-20 GB storage
  - Automatic backups
  - Dedicated database

## Custom Domain

1. Buy domain (GoDaddy, Namecheap, etc.)
2. In Render, go to service settings
3. Add custom domain
4. Update DNS settings per Render instructions
5. Free SSL certificate auto-generates

## Next Steps

✅ Deployed to Render  
📊 Monitor at `https://your-domain.com/`  
🧪 Test at `https://your-domain.com/test.html`  
📈 Dashboard at `https://your-domain.com/dashboard.html`  

For more help, see:
- `DEPLOYMENT.md` - Advanced deployment options
- `API_REFERENCE.md` - API documentation
- `MULTI_AGENT_GUIDE.md` - Multi-agent workflows
