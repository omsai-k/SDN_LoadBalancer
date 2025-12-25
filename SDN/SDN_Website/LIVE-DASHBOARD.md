# 🌉 Live Dashboard Connection Guide

## The Solution: Bridge API

You now have a **Bridge API** that connects your dashboard directly to the real SDN controller!

### Architecture

```
Your Terminal Clients
         ↓
   Send Requests
         ↓
  SDN Controller (5000)
         ↓
   Bridge API (9000) ← NEW!
         ↓
  Web Dashboard (8000)
```

---

## 🚀 How It Works

### Step 1: Start Everything
```bash
cd /Users/omsai/Documents/OS/projects/SDN/SDN_Website
./setup-full-network.sh
```

Starts:
- Backend Servers (8001, 8002, 8003)
- SDN Controller (5000)
- **Bridge API (9000)** ← Fetches real data
- Dashboard (8000)

### Step 2: Open Dashboard
```
http://localhost:8000
```

The dashboard connects to Bridge API on port 9000, which reads from the real controller.

### Step 3: Send Traffic
```bash
cd /Users/omsai/Documents/OS/projects/SDN/SDN_LoadBalancer

# Send 100 requests
for i in {1..100}; do 
  curl -s -X POST http://localhost:5000/balance \
    -H "Content-Type: application/json" \
    -d "{\"flow\": {\"id\": $i}}" &
done
wait
```

### Step 4: Watch Dashboard Update in Real-Time
The **Load Balancing** page will show:
- ✅ Real request count increasing
- ✅ Real utilization changing
- ✅ Real response times
- ✅ Actual backend loads
- ✅ Threat detection alerts

---

## 📊 What Updates in Real-Time

### Dashboard Page
- Live throughput (Mbps)
- Active connections
- Packet count
- Network latency
- Packet loss percentage

### Load Balancing Page
- **Active Load Balancers** - Real count
- **Average Utilization** - Actual % 
- **Avg Response Time** - Real latency
- **Failed Connections** - Actual errors
- **Backend Load Distribution** - Real server loads

### Threat Detection Page
- Detected threat level
- Anomaly detection
- Packet analysis
- Bytes analyzed

---

## 🔍 Bridge API Endpoints

All running on port 9000:

```
GET  /api/stats                    - Real network statistics
GET  /api/load-balancing/status    - Load balancer info
GET  /api/threat-detection/status  - Threat alerts
GET  /api/metrics/history          - Historical data
GET  /api/network/topology         - Network structure
GET  /api/dashboard/summary        - Dashboard summary
GET  /api/health                   - Health check
GET  /api/test                     - Test connection
```

---

## 🧪 Test It Now

### Terminal 1: Start Network
```bash
./setup-full-network.sh
```

Wait for all services to start (you'll see confirmation messages).

### Terminal 2: Open Browser
```
http://localhost:8000
```

Go to **Load Balancing** page.

### Terminal 3: Send Traffic
```bash
cd /Users/omsai/Documents/OS/projects/SDN/SDN_LoadBalancer

# Single request
curl -X POST http://localhost:5000/balance \
  -H "Content-Type: application/json" \
  -d '{"flow": {"id": 1}}'
```

### Watch
The dashboard will update immediately with:
- Request count increased
- Load percentage updated
- Response times displayed

---

## 💡 Key Features

✅ **Real-Time Updates** - Every 1 second  
✅ **No Static Data** - All from actual controller  
✅ **Live Traffic Monitoring** - See requests as they flow  
✅ **Real Threat Detection** - Detects actual anomalies  
✅ **Automatic Failover** - Falls back to simulated if needed  
✅ **Multiple Clients Supported** - Send traffic from multiple terminals  

---

## 🎯 What You Can Do

1. **Stress Test**
```bash
for i in {1..1000}; do 
  curl -s -X POST http://localhost:5000/balance \
    -H "Content-Type: application/json" \
    -d "{\"flow\": {\"id\": $i}}" &
done
wait
```
Watch dashboard show high load and utilization!

2. **Concurrent Clients**
```bash
# Terminal 1
python3 << 'EOF'
import requests
for i in range(500):
    requests.post('http://localhost:5000/balance', json={"flow": {"id": i}})
EOF

# Terminal 2
python3 << 'EOF'
import requests
for i in range(500):
    requests.post('http://localhost:5000/balance', json={"flow": {"id": i}})
EOF
```
Watch how load balancing distributes across servers!

3. **Threat Detection**
```bash
curl -X POST http://localhost:5000/detect_threat \
  -H "Content-Type: application/json" \
  -d '{"packets": 50000, "bytes": 5000000}'
```
Dashboard will show threat alerts!

---

## 🛠️ Manual Start (If Preferred)

Instead of `setup-full-network.sh`, you can run each service manually:

**Terminal 1: Backend 1**
```bash
cd SDN_LoadBalancer && python3 backend_server.py 8001
```

**Terminal 2: Backend 2**
```bash
cd SDN_LoadBalancer && python3 backend_server.py 8002
```

**Terminal 3: Backend 3**
```bash
cd SDN_LoadBalancer && python3 backend_server.py 8003
```

**Terminal 4: Controller**
```bash
cd SDN_LoadBalancer && python3 run.py
```

**Terminal 5: Bridge API**
```bash
cd SDN_Website && python3 bridge_api.py
```

**Terminal 6: Dashboard**
```bash
cd SDN_Website && python3 -m http.server 8000
```

**Terminal 7: Send Traffic**
```bash
# Your traffic generation commands
```

---

## ✅ Verification

To verify everything is connected:

1. **Check Bridge API**
```bash
curl http://localhost:9000/api/health
```
Should return: `{"status": "ok", "bridge_api": "running", "controller": "connected"}`

2. **Check Controller**
```bash
curl http://localhost:5000/health
```

3. **Check Dashboard**
Open `http://localhost:8000` and refresh

---

## 🎊 That's It!

You now have:
- ✅ Real SDN network running
- ✅ Multiple backend servers
- ✅ Working load balancer
- ✅ Real-time dashboard
- ✅ Live threat detection

**The dashboard is no longer static - it's LIVE!** 🚀

Send traffic from terminals and watch the dashboard update in real-time with actual data.

---

## 📝 Files Modified

- `bridge_api.py` - NEW: Connects dashboard to controller
- `js/api-client.js` - Updated to use bridge API
- `setup-full-network.sh` - Now starts bridge API
- `REAL-NETWORK-SETUP.md` - Updated with bridge info

Start with: `./setup-full-network.sh`
