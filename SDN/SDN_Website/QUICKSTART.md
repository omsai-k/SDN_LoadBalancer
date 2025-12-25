# 🚀 SDN Management Platform - Quick Start Guide

## Welcome! 👋

This guide will get you up and running with the SDN Management Platform in minutes.

## Step 1: Install Dependencies (First Time Only)

Open Terminal and run:

```bash
cd /Users/omsai/Documents/OS/projects/SDN/SDN_Website
chmod +x start.sh
pip3 install -r requirements.txt
```

## Step 2: Start All Services

**Option A: One-Command Startup (Recommended)**
```bash
./start.sh
```

**Option B: Manual Startup**

Terminal 1 - API Server:
```bash
cd /Users/omsai/Documents/OS/projects/SDN/SDN_Website
python3 sdn_api_server.py
```

Terminal 2 - Web Server:
```bash
cd /Users/omsai/Documents/OS/projects/SDN/SDN_Website
python3 -m http.server 8000
```

## Step 3: Open the Platform

Open your browser and go to:
```
http://localhost:8000
```

You should see the **Network Overview Dashboard** 🎯

## 🎮 What You Can Do

### 1. Monitor Network in Real-Time ✅
- Dashboard shows live network statistics
- View active threats and alerts
- Monitor all connected switches and controllers

### 2. Simulate Network Attacks 🎯
Go to **Security Control** → **Attack Simulator**:
1. Select an attack type (9 available)
2. Enter source IP
3. Choose target
4. Set duration
5. Click "Launch Attack"
6. Watch threats appear in real-time!

**Available Attack Types:**
- 🔴 DDoS - Overwhelm network with traffic
- 🔴 Port Scan - Scan for open ports
- 🟠 SYN Flood - TCP connection flood
- 🟠 Brute Force - Credential guessing
- 🟡 SQL Injection - Database attacks
- 🟡 Malware - Malicious code simulation
- 🟢 Unauthorized Access - Break-in attempts
- 🟢 Bandwidth Spike - Traffic surge
- 🔵 Anomalous Traffic - Unusual patterns

### 3. Block Malicious IPs 🚫
Go to **Security Control** → **IP Management**:
1. Enter any IP address
2. Click "Block IP"
3. See it added to blocked list
4. Click "Unblock" to remove

### 4. Explore All Pages
- **Dashboard**: Overall network health
- **Topology**: Network architecture visualization
- **Threat Detection**: View and respond to threats
- **Load Balancing**: See server load distribution
- **Analytics**: Traffic analysis and trends
- **Controllers**: Manage SDN controllers
- **Settings**: Platform configuration

## 🧪 Quick Demo Scenario

Try this demo to see everything in action:

**5-Minute Demo:**
1. Open Dashboard - note the current network stats
2. Go to Security Control
3. Click "DDoS (5min)" quick template
4. Watch the dashboard update in real-time
5. See threat appear in Threat Detection
6. Go to IP Management and block the attacking IP
7. Watch the threat get mitigated!

## 🔧 Keyboard Shortcuts & Quick Navigation

| Action | Shortcut |
|--------|----------|
| Refresh Stats | Click "Refresh" button |
| New Attack | Click any Quick Template |
| View Threats | Go to Threat Detection page |
| Block IP | Security Control → IP Management |
| Check Logs | F12 (Browser Console) |

## 📊 Real-Time Features

- ✅ Stats update every 2-3 seconds
- ✅ WebSocket provides instant notifications
- ✅ Threat alerts appear immediately
- ✅ IP blocking takes effect instantly
- ✅ Dashboard auto-refreshes without page reload

## 🆘 Troubleshooting

### "Connection Failed" Error
1. Make sure API server is running (Terminal 1)
2. Make sure Web server is running (Terminal 2)
3. Check http://localhost:5000/api/health in browser
4. Refresh the page (Ctrl+R or Cmd+R)

### No Threats Appearing After Attack
1. Click "Launch Attack" button (not just template)
2. Check browser console (F12) for errors
3. Wait 2-3 seconds for WebSocket update
4. Try refreshing the page

### Python Error: "ModuleNotFoundError"
```bash
pip3 install --upgrade -r requirements.txt
```

### Ports Already in Use
Kill existing processes:
```bash
# Kill API (port 5000)
lsof -i :5000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Kill Web (port 8000)
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

## 📈 What's Happening Behind the Scenes

**API Server (Port 5000):**
- Manages network state
- Simulates attacks
- Tracks blocked IPs
- Sends real-time updates via WebSocket

**Web Server (Port 8000):**
- Serves HTML/CSS/JS pages
- No database - all in-memory

**Browser (Client):**
- Displays real-time data
- Handles user interactions
- Connects via WebSocket for instant updates

## 🎓 Learning Path

**Beginner:**
1. Explore Dashboard
2. Navigate through all pages
3. Observe real-time updates

**Intermediate:**
1. Launch some attacks
2. View threats in detail
3. Block attacking IPs

**Advanced:**
1. Open Browser DevTools (F12)
2. Watch Network tab for API calls
3. Check Console for logs
4. Look at WebSocket messages
5. Customize attack parameters

## 📱 Browser Support

Works on:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## 🚨 Important Notes

1. **This is a simulation** - Not connected to real networks
2. **Attacks are simulated** - No actual network harm
3. **Data is in-memory** - Resets on server restart
4. **Educational use** - Perfect for learning SDN concepts

## 💡 Pro Tips

1. **Watch the Console**: Open F12 → Console to see what's happening
2. **Check Network Tab**: See real-time API calls
3. **Multiple Attacks**: You can run multiple attacks simultaneously
4. **Long Attacks**: Try a 600-second attack and let it run while exploring
5. **Refresh Everything**: Sometimes Ctrl+R is your best friend

## 🎯 Next Steps

1. ✅ Start the platform
2. ✅ Explore all pages
3. ✅ Launch an attack
4. ✅ Block some IPs
5. ✅ Check the API endpoints
6. ✅ Read the full README.md
7. ✅ Check the source code
8. ✅ Modify and experiment!

## 📞 Need Help?

1. Check the **full README.md** for detailed documentation
2. Open **Developer Tools** (F12) to see logs
3. Check **http://localhost:5000/api/health** to verify API
4. Look at **sdn_api_server.py** to understand the backend
5. Look at **js/api-client.js** to understand the frontend

---

**Ready to go?** Run `./start.sh` and open **http://localhost:8000** 🚀

Enjoy exploring the SDN Management Platform!
