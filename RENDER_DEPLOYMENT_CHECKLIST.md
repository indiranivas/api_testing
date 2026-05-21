# Render Deployment Checklist

Complete step-by-step checklist for deploying to Render.

## Pre-Deployment Checklist

- [ ] Repository is on GitHub
- [ ] All files committed and pushed
  ```bash
  git add .
  git commit -m "Ready for Render deployment"
  git push origin main
  ```
- [ ] `.env` file is in `.gitignore` (NOT committed)
- [ ] `render.yaml` exists in project root
- [ ] `requirements.txt` includes: fastapi, uvicorn, sqlalchemy, python-dotenv, gunicorn, psycopg2-binary
- [ ] `main.py` includes environment variable loading:
  ```python
  from dotenv import load_dotenv
  load_dotenv()
  ```
- [ ] Frontend files (index.html, test.html, dashboard.html) exist
- [ ] All static files use dynamic API URL:
  ```javascript
  const API_URL = window.location.origin;
  ```

## Files Verification

Required files:
```
✓ main.py (FastAPI backend)
✓ requirements.txt (dependencies)
✓ render.yaml (Render configuration)
✓ index.html (home page)
✓ test.html (testing interface)
✓ dashboard.html (monitoring dashboard)
```

Not committed (should be in .gitignore):
```
✓ .env (local environment - NOT on GitHub)
✓ telemetry.db (database)
✓ __pycache__/ (Python cache)
✓ .venv/ (virtual environment)
```

## Render Setup Steps

### Step 1: Render Account Setup
- [ ] Create Render account at https://render.com
- [ ] Verify email
- [ ] Add payment method (if using paid plan)

### Step 2: Connect GitHub
- [ ] Go to Render dashboard
- [ ] Click "New +" → "Web Service"
- [ ] Click "Connect Account"
- [ ] Authorize GitHub
- [ ] Select your repository
- [ ] Click "Connect"

### Step 3: Service Configuration
- [ ] Service name: `telemetry-system`
- [ ] Runtime: Python 3.9 (auto-detected)
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `gunicorn main:app --workers 3 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
- [ ] Plan: Free (or paid if needed)

**Note:** render.yaml will be auto-detected - verify above settings match

### Step 4: Environment Variables
Render auto-sets from render.yaml:
- [ ] `DATABASE_URL=sqlite:///./telemetry.db`
- [ ] `DEBUG=false`
- [ ] `PYTHONUNBUFFERED=1`

**Optional:** For PostgreSQL database:
- [ ] Create PostgreSQL database in Render (click "New +" → "PostgreSQL")
- [ ] Copy connection string
- [ ] Update `DATABASE_URL` in web service environment

### Step 5: Deploy
- [ ] Click "Create Web Service"
- [ ] Monitor "Logs" tab for build/startup messages
- [ ] Wait for "Your service is live!"
- [ ] Copy service URL (e.g., https://telemetry-system.onrender.com)

## Post-Deployment Verification

### Test Deployment
- [ ] Access home page: `https://telemetry-system.onrender.com/`
- [ ] Check backend status (should show green ✓)
- [ ] Go to Testing: `https://telemetry-system.onrender.com/test.html`
- [ ] Send a test event
- [ ] Go to Dashboard: `https://telemetry-system.onrender.com/dashboard.html`
- [ ] Verify event appears in dashboard
- [ ] Check API responds: `curl https://telemetry-system.onrender.com/health`

### Monitor Logs
- [ ] Check Render "Logs" tab for errors
- [ ] Look for successful startup message:
  ```
  INFO: Application startup complete
  ```
- [ ] Monitor for connection errors

### Test Key Features
- [ ] Home page loads
- [ ] Navigation works (links between pages)
- [ ] Testing page: Send single event
- [ ] Testing page: Run demo scenario
- [ ] Dashboard: Auto-refresh works
- [ ] Dashboard: Shows sessions and events
- [ ] Dashboard: Metrics are accurate

## Common Issues & Solutions

### Build Fails

**Issue:** Docker build fails
- [ ] Check `requirements.txt` format
- [ ] Verify no syntax errors in files
- [ ] Look at Render logs for specific error

**Fix:**
```bash
# Test locally first
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### 502 Bad Gateway

**Issue:** Service returns 502 errors
- [ ] Service still starting (wait 2-3 minutes)
- [ ] Port mismatch
- [ ] Out of memory

**Fix:**
- [ ] Wait for service to fully start
- [ ] Check logs for errors
- [ ] Upgrade to paid plan for more resources

### Database Errors

**Issue:** SQLite errors or database locked
- [ ] Render's file system is ephemeral (data lost on restart!)
- [ ] Better to use PostgreSQL

**Fix:**
- [ ] Create PostgreSQL database in Render
- [ ] Update `DATABASE_URL` environment variable
- [ ] Restart service

### Static Files Not Loading

**Issue:** 404 errors for CSS, images, or pages
- [ ] Files not in project root
- [ ] Incorrect file names
- [ ] main.py not serving static files

**Fix:**
- [ ] Verify HTML files exist: index.html, test.html, dashboard.html
- [ ] Check main.py has:
  ```python
  from fastapi.staticfiles import StaticFiles
  app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
  ```
- [ ] Restart service in Render

### CORS Errors

**Issue:** Browser blocks API calls
- [ ] CORS not enabled in main.py
- [ ] Wrong origin in request

**Fix:**
- [ ] Verify main.py has CORSMiddleware
- [ ] Verify `allow_origins=["*"]`
- [ ] Check browser console (F12) for specific error

## Monitoring & Maintenance

### Daily Checks (First Week)
- [ ] Monday: Check logs for errors
- [ ] Wednesday: Test sending events
- [ ] Friday: Verify dashboard updates

### Weekly Checks (After First Week)
- [ ] Check Render Metrics tab
- [ ] CPU usage normal? (< 50%)
- [ ] Memory usage normal? (< 200MB)
- [ ] Response times acceptable?

### Monthly Maintenance
- [ ] Review logs for errors/warnings
- [ ] Test all features still working
- [ ] Backup database (if using PostgreSQL)
- [ ] Update dependencies if needed

### Database Management
- [ ] For PostgreSQL: Enable automatic backups
- [ ] For SQLite: Schedule manual backups (not recommended)
- [ ] Monitor database size
- [ ] Plan for data retention policy

## Scaling Steps

If you hit limits:

### Increase Resources
- [ ] Go to service settings
- [ ] Click "Instance Type"
- [ ] Upgrade from Free to Starter ($7/month)
- [ ] Provides: 24/7 uptime, more resources, custom domain

### Load Balancing
- [ ] Create multiple service instances
- [ ] Use Render's native load balancing
- [ ] Monitor with Metrics tab

### Use PostgreSQL
- [ ] Create PostgreSQL database
- [ ] Update DATABASE_URL
- [ ] Supports full backups
- [ ] Better for concurrent users

## Cost Overview

| Plan | Price | Features |
|------|-------|----------|
| Free | $0 | 750 hrs/month, 0.5GB RAM, auto-sleeps |
| Starter | $7/month | 24/7 uptime, 1GB RAM, custom domain |
| Pro | $25+ | 2GB RAM, priority support |
| PostgreSQL | $7-15/month | Database + backups |

## Maintenance Scripts

### Monitor Service Health
```bash
# Add to cron job (checks every hour)
0 * * * * curl https://telemetry-system.onrender.com/health >> /var/log/health.log
```

### Backup (for SQLite - not recommended)
```bash
# Manual backup via Render shell
# Better to use PostgreSQL with auto-backups
```

## Post-Deployment Steps

### Custom Domain (Optional)
- [ ] Buy domain (GoDaddy, Namecheap, etc.)
- [ ] In Render settings, add custom domain
- [ ] Update DNS to point to Render
- [ ] SSL certificate auto-generates

### Auto-Deploy from GitHub
- [ ] In Render service settings
- [ ] Enable "Auto-deploy" from main branch
- [ ] Now every git push auto-deploys

### Monitoring & Alerts (Optional)
- [ ] Setup health check monitoring
- [ ] Email alerts on failure
- [ ] Track metrics over time

### Analytics (Optional)
- [ ] Add Google Analytics to HTML files
- [ ] Track user activity
- [ ] Monitor usage patterns

## Success Criteria

✅ System is "live" (Render shows deployed status)
✅ Home page loads at service URL
✅ Backend health check returns 200 OK
✅ Can send test events from Testing page
✅ Events appear in Dashboard within 2 seconds
✅ All pages load without 404 errors
✅ CSS and styling looks correct
✅ Auto-refresh works on dashboard
✅ No errors in browser console (F12)
✅ Metrics display accurate counts

## Next Steps After Deployment

1. **Monitor** - Watch logs and metrics daily
2. **Test** - Regular testing via Testing page
3. **Document** - Note your service URL for team
4. **Integrate** - Connect real agents/workflows
5. **Scale** - Add PostgreSQL if needed
6. **Maintain** - Check health weekly

## Support Resources

- Render Docs: https://render.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com/
- GitHub: Push code changes to auto-deploy
- Email: Support within Render dashboard

## Deployment Date Record

- **Deployment Date:** _____________
- **Service URL:** _____________
- **Database Type:** [ ] SQLite [ ] PostgreSQL
- **Plan:** [ ] Free [ ] Starter [ ] Other
- **Notes:** _____________

---

✅ **All checks complete? You're ready for production!**

Questions? Check:
1. RENDER_SETUP.md
2. ENVIRONMENT_SETUP.md
3. DEPLOYMENT.md
