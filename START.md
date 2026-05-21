# Quick Start Guide

## 🚀 Run Locally (2 Minutes)

### Terminal 1: Start Backend

```bash
cd telemetry_sdk
pip install -r requirements.txt
uvicorn main:app --reload
```

Wait for: `Uvicorn running on http://127.0.0.1:8000`

### Terminal 2: Start Web Server

```bash
cd telemetry_sdk
python run_dashboard.py
```

Your browser will open automatically to:
```
http://localhost:8001/
```

---

## 📍 Access Points

| What | Where |
|------|-------|
| **Home Page** | `http://localhost:8001/` |
| **Send Telemetry** | `http://localhost:8001/test.html` |
| **Monitor Dashboard** | `http://localhost:8001/dashboard.html` |
| **API** | `http://127.0.0.1:8000` |

---

## 🧪 Test It

1. Go to **Testing** page
2. Click **"Send Single Event"** or **"Run Demo (4 Agents)"**
3. Switch to **Dashboard** to see results in real-time ✨

---

## 📦 Production Hosting

See `HOSTING.md` for:
- Docker deployment
- Linux server setup
- Cloud platforms (AWS, Azure, Google Cloud)
- Nginx reverse proxy
- HTTPS/SSL setup

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| `HOSTING.md` | How to host/deploy |
| `DEPLOYMENT.md` | Detailed deployment guide |
| `API_REFERENCE.md` | API endpoint documentation |
| `README.md` | Overview & database schema |

---

## ✅ Quick Checklist

- [ ] Python 3.7+ installed
- [ ] `pip install -r requirements.txt` done
- [ ] Backend running on port 8000
- [ ] Web server running on port 8001
- [ ] Home page loads at `http://localhost:8001/`
- [ ] Can send test telemetry
- [ ] Dashboard updates in real-time

---

## 🆘 Troubleshooting

**Port already in use?**
```bash
# Find process on port 8001
lsof -i :8001

# Kill it
kill -9 <PID>
```

**Module not found?**
```bash
pip install -r requirements.txt
```

**Can't connect to backend?**
```bash
# Check if backend is running
curl http://127.0.0.1:8000/health
```

---

## 📞 Support

Check these files:
1. `DEPLOYMENT.md` - Detailed setup guide
2. `API_REFERENCE.md` - API documentation
3. `HOSTING.md` - Hosting options
4. `MULTI_AGENT_GUIDE.md` - Multi-agent workflows

---

**Ready? Start the servers and visit:** 🏠 `http://localhost:8001/`

