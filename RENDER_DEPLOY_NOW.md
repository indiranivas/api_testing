# Render Deployment - START HERE

Simple single-service deployment. Follow these exact steps.

## 3 Steps - Takes 5 Minutes

### Step 1: Push to GitHub

```bash
cd telemetry_sdk
git add .
git commit -m "Ready for Render"
git push origin main
```

### Step 2: Create Web Service on Render

1. Go to **https://dashboard.render.com**
2. Click **"New +"** → **"Web Service"**
3. Select your GitHub repository
4. Click **"Connect"**

### Step 3: Configure (Copy These Exact Values)

| Field | Value |
|-------|-------|
| Name | `telemetry-system` |
| Runtime | `Python 3.9` |
| Build | `pip install -r requirements.txt` |
| Start | `gunicorn main:app --workers 3 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT` |
| Plan | Free |

Click **"Create Web Service"**

Wait 2-5 minutes. Done! 🎉

---

## Access Your System

```
Home:      https://telemetry-system-xxxxx.onrender.com/
Test:      https://telemetry-system-xxxxx.onrender.com/test.html
Dashboard: https://telemetry-system-xxxxx.onrender.com/dashboard.html
```

(Replace `xxxxx` with your service name)

---

## Test It

1. Visit home page
2. Check backend shows ✓
3. Go to Testing
4. Send test event
5. Go to Dashboard
6. See event appear ✓

---

## What You Just Deployed

```
One Render Service:
├─ FastAPI backend (serves API)
├─ Static files (HTML/CSS/JS)
├─ SQLite database (auto-created)
└─ Everything works together!
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| 502 errors | Wait 3 min - service starting |
| 404 on pages | HTML files must be in root |
| No backend status | Check logs in Render dashboard |
| API calls fail | Check browser console (F12) |

---

## Logs & Monitoring

In Render dashboard:
- Click service → "Logs" tab
- See all startup messages and errors
- Check for problems

---

## Update Code Later

```bash
git add .
git commit -m "Update something"
git push origin main
```

Go to Render dashboard → service → click "Manual Deploy" (or enable auto-deploy)

---

## Success Checklist

- [ ] Service shows "Your service is live"
- [ ] Home page loads
- [ ] Backend status shows ✓
- [ ] Can send test events
- [ ] Dashboard displays data
- [ ] No errors in logs

✅ **All checked? You're done!** Your telemetry system is live on Render! 🚀

---

For more details: Read `RENDER_SINGLE_SERVICE.md`
