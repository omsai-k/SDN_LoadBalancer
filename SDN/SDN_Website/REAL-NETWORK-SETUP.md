# 🚀 Real SDN Network Setup Guide

## Overview

You have **two setup options**:

### Option 1: Simulated Network (Dashboard Only)
- Everything in-memory, no real backend needed
- Perfect for quick demos
- Start with: `./start.sh`

### Option 2: Real Network (What You Want!)
- 3 actual backend servers
- Real SDN controller
- Dashboard connecting to real controller
- Send real traffic and attacks
- **Start with: See below** 👇

---

## 🎯 Complete Real Network Setup

### Terminal 1: Start All Services at Once

```bash
cd /Users/omsai/Documents/OS/projects/SDN/SDN_Website
chmod +x setup-full-network.sh
./setup-full-network.sh
```

This starts:
- ✅ 3 Backend Servers (ports 8001, 8002, 8003)
- ✅ SDN Controller (port 5000)
- ✅ **Bridge API** (port 9000) - Connects dashboard to real controller 🌉
- ✅ Web Dashboard (port 8000)

### Open Browser
```
http://localhost:8000
```

**The dashboard will now show REAL data from the actual network as you send traffic!**

---

## 🖥️ Manual Setup (Terminal by Terminal)

If you want more control, open 5 terminals:

### Terminal 1: Backend Server 1
```bash
cd /Users/omsai/Documents/OS/projects/SDN/SDN_LoadBalancer
python3 backend_server.py 8001
```

### Terminal 2: Backend Server 2
```bash
cd /Users/omsai/Documents/OS/projects/SDN/SDN_LoadBalancer
python3 backend_server.py 8002
```

### Terminal 3: Backend Server 3
```bash
cd /Users/omsai/Documents/OS/projects/SDN/SDN_LoadBalancer
python3 backend_server.py 8003
```

### Terminal 4: SDN Controller/Load Balancer
```bash
cd /Users/omsai/Documents/OS/projects/SDN/SDN_LoadBalancer
export BACKENDS="http://localhost:8001,http://localhost:8002,http://localhost:8003"
python3 run.py
```

### Terminal 5: Web Dashboard
```bash
cd /Users/omsai/Documents/OS/projects/SDN/SDN_Website
python3 -m http.server 8000
```

---

## 🧪 Test the Network

### Terminal 6: Send Test Traffic

**Option A: Run demo client**
```bash
cd /Users/omsai/Documents/OS/projects/SDN/SDN_LoadBalancer
python3 demo_client.py
```

**Option B: Send requests manually**
```bash
# Single request
curl -X POST http://localhost:5000/balance \
  -H "Content-Type: application/json" \
  -d '{"flow": {"id": 1, "source": "192.168.1.1", "destination": "192.168.1.2"}}'

# Load test (100 requests)
for i in {1..100}; do 
  curl -s -X POST http://localhost:5000/balance \
    -H "Content-Type: application/json" \
    -d "{\"flow\": {\"id\": $i}}" &
done
wait

# Threat detection test
curl -X POST http://localhost:5000/detect_threat \
  -H "Content-Type: application/json" \
  -d '{"packets": 10000, "bytes": 1000000}'
```

**Option C: Python attack client**
```bash
python3 << 'EOF'
import requests
import time
from threading import Thread

def send_attack(duration=30):
    """Send continuous attack traffic"""
    start = time.time()
    count = 0
    while time.time() - start < duration:
        try:
            requests.post('http://localhost:5000/balance', 
                         json={"flow": {"id": count}},
                         timeout=1)
            count += 1
        except:
            pass
        time.sleep(0.01)  # 100 requests/sec
    print(f"Sent {count} requests in {duration}s")

# Run attack in background
threads = [Thread(target=send_attack, args=(60,)) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
EOF
```

---

## 📊 Architecture

```
                    Dashboard (8000)
                          ↑
                    HTML/CSS/JavaScript
                          ↓
    Load Balancer/Controller (5000)
            ↓        ↓        ↓
        Backend1  Backend2  Backend3
        (8001)    (8002)    (8003)
          ↓         ↓         ↓
      Server1    Server2    Server3
```

---

## 🎮 What You Can Do

1. **View Dashboard** - See real-time load balancing
2. **Send Traffic** - Generate requests from terminal
3. **Monitor Threats** - See threat detection in action
4. **Test Load Balancing** - Observe distribution across servers
5. **Attack Simulation** - Send high-volume or malformed traffic
6. **Check Statistics** - View throughput, latency, packet loss

---

## 📈 Monitor in Dashboard

While clients are sending traffic:

1. Open `http://localhost:8000`
2. Go to **Dashboard** to see:
   - Real-time throughput
   - Active connections
   - Server load distribution
3. Go to **Load Balancing** to see:
   - Which server each request goes to
   - Load distribution chart
4. Go to **Threat Detection** to see:
   - Detected anomalies
   - Threat alerts

---

## 🛑 Stop All Services

```bash
# If using setup-full-network.sh:
# Just press Ctrl+C

# If manual setup:
# Press Ctrl+C in each terminal
```

Or in one command:
```bash
pkill -f "backend_server.py\|run.py\|http.server"
```

---

## 🐛 Troubleshooting

### Port already in use
```bash
# Check what's using port 5000
lsof -i :5000

# Kill it
lsof -i :5000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### Backend servers not connecting
- Make sure all 3 backend servers started successfully
- Check they're on ports 8001, 8002, 8003
- Controller should see them in logs

### Dashboard shows no data
- Verify controller is running on port 5000
- Send some test traffic first
- Check browser console (F12) for errors
- Try refreshing page

### Clients can't connect
- Verify controller is running (`curl http://localhost:5000/api/health`)
- Check firewall allows localhost connections
- Make sure you're using correct URL

---

## 🎯 Quick Test Sequence

1. **Terminal 1:** `./setup-full-network.sh`
   - Wait for all services to start
2. **Browser:** Open `http://localhost:8000`
   - Should see dashboard loading
3. **Terminal 2:** 
   ```bash
   cd /Users/omsai/Documents/OS/projects/SDN/SDN_LoadBalancer
   python3 demo_client.py
   ```
4. **Watch Dashboard** - See traffic flowing
5. **Try attacks** - Send high-volume requests
6. **Monitor** - Observe threat detection

---

## 📝 Environment Variables

In case you need to customize:

```bash
# For controller
export BACKENDS="http://localhost:8001,http://localhost:8002,http://localhost:8003"
export HOST="0.0.0.0"
export PORT=5000
export LOG_LEVEL="INFO"

# Then run
python3 run.py
```

---

## ✅ You're Ready!

You now have:
- Real network with 3 backend servers
- Working SDN controller
- Dashboard to monitor it
- Ability to send attacks and test

Start with: `./setup-full-network.sh` 🚀
