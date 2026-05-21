# Render Deployment - Quick Start (5 Minutes)

Deploy the telemetry system to Render.com instantly.

## Prerequisites

✓ GitHub repository with code  
✓ Render.com account (free)  
✓ Files include: `render.yaml`, `main.py`, HTML files  

## Step 1: Push to GitHub

```bash
git add .
git commit -m "Ready for Render"
git push origin main
```

## Step 2: Create Web Service on Render

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect Account"** (authorize GitHub)
4. Select your repository
5. Click **"Connect"**
6. Render auto-detects `render.yaml` settings
7. Click **"Create Web Service"**

## Step 3: Wait for Deployment

Watch the "Logs" tab:
```
Building...
Installing dependencies...
Starting service...
✓ Your service is live!
```

This takes 2-5 minutes.

## Step 4: Access Your System

Once deployed, Render shows your URL: `https://telemetry-system.onrender.com`

Visit:
- **Home:** https://telemetry-system.onrender.com/
- **Testing:** https://telemetry-system.onrender.com/test.html
- **Dashboard:** https://telemetry-system.onrender.com/dashboard.html

## That's It! 🎉

Your system is now live on the internet. Anyone can access it via the URL.

---

## What's Running?

```
render.yaml configures:
├─ Build: pip install requirements.txt
├─ Start: gunicorn (FastAPI server)
├─ Port: Auto-assigned by Render
├─ Database: SQLite (auto-created)
└─ Static Files: HTML served by FastAPI
```

## Quick Test

1. Visit home page
2. Check "Backend is running ✓"
3. Go to Testing page
4. Send a test event
5. Go to Dashboard
6. See event in real-time! ✨

## Common Issues

| Issue | Solution |
|-------|----------|
| 502 errors | Service still starting - wait 2 min |
| 404 errors | Check HTML files exist |
| DB errors | Normal for SQLite - data persists |
| CORS errors | API should respond - check logs |

## Upgrade to Production (Optional)

Free plan has limits. To run 24/7:

1. In Render dashboard
2. Go to service settings
3. Change plan to **"Starter"** ($7/month)
4. Includes: custom domain, auto-deploy, more resources

## Auto-Deploy on Git Push

1. Go to service settings
2. Enable **"Auto-deploy"**
3. Now every `git push` deploys automatically!

## Monitor Your Service

In Render dashboard:
- **Logs** - See startup messages and errors
- **Metrics** - CPU, memory, network usage
- **Events** - Deployment history

## Add Custom Domain

1. Buy domain (GoDaddy, Namecheap, etc.)
2. In Render: Add custom domain
3. Update DNS per instructions
4. Free SSL certificate auto-generates

## Logs

```bash
# Check logs in Render dashboard
# Or use curl to test:
curl https://telemetry-system.onrender.com/health

# Should return:
{"status": "healthy"}
```

## Next Steps

✅ Deployed!  
📊 Monitor at https://your-url/  
🧪 Test at https://your-url/test.html  
📈 Dashboard at https://your-url/dashboard.html  

For more:
- `RENDER_SETUP.md` - Detailed guide
- `RENDER_DEPLOYMENT_CHECKLIST.md` - Verification checklist
- `ENVIRONMENT_SETUP.md` - Configuration details
- Render Docs: https://render.com/docs

---

**Your telemetry system is now live!** 🚀
