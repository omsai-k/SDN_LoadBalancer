# 🔧 Configuration & Deployment Guide

## Overview

This guide covers all configuration options and deployment scenarios for the SDN Management Platform.

---

## 🎛️ Configuration Options

### Environment Variables (Optional)

Create a `.env` file in the project root to customize:

```bash
# API Server Configuration
FLASK_HOST=0.0.0.0              # Default: localhost
FLASK_PORT=5000                 # Default: 5000
FLASK_DEBUG=1                   # 0 or 1, default: 0

# WebSocket Configuration
SOCKETIO_PING_TIMEOUT=60        # Seconds
SOCKETIO_PING_INTERVAL=25       # Seconds

# Network Simulation
NETWORK_UPDATE_INTERVAL=2       # Seconds between updates
ATTACK_HISTORY_SIZE=100         # Max attacks to track
METRICS_HISTORY_SIZE=1000       # Max metrics to store

# Threat Detection
AUTO_BLOCK_ON_THREAT=1          # Auto block attacking IPs (1 or 0)
THREAT_SEVERITY_THRESHOLD=low   # low, medium, high, critical
```

### Modify API Server (sdn_api_server.py)

**Key Configuration Points:**

```python
# Line 15-20: Network Parameters
NETWORK_UPDATE_INTERVAL = 2          # How often to update stats
ATTACK_HISTORY_MAX_SIZE = 100        # Attack history limit

# Line 30-35: Attack Types
ATTACK_TYPES = {
    'ddos', 'port_scan', 'syn_flood',
    'brute_force', 'sql_injection', 'malware',
    'unauthorized_access', 'bandwidth_spike', 'anomalous_traffic'
}

# Line 50-100: generate_network_stats()
# Modify here to change metric ranges and patterns

# Line 200+: Route configurations
# Modify here to add new API endpoints
```

### Modify Frontend (js/api-client.js)

**Key Configuration Points:**

```javascript
// Line 5: API Server URL
const API_BASE_URL = 'http://localhost:5000';

// Line 10-20: WebSocket Options
socket = io(API_BASE_URL, {
    reconnection: true,
    reconnectionDelay: 1000,        // Initial delay
    reconnectionDelayMax: 5000,     // Max delay
    reconnectionAttempts: 5         // Retry count
});

// Line 80+: Polling Configuration (if WebSocket unavailable)
// setInterval(fetchStats, 2000);   // Update every 2 seconds
```

---

## 🚀 Deployment Scenarios

### Scenario 1: Development (Local Machine)

**Best for:** Testing, learning, development

```bash
# Setup
cd /Users/omsai/Documents/OS/projects/SDN/SDN_Website
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run
python3 sdn_api_server.py &
python3 -m http.server 8000 &

# Access
# Browser: http://localhost:8000
# API: http://localhost:5000
```

### Scenario 2: Network Deployment

**Best for:** Multiple machines, team testing

Machine 1 (API Server):
```bash
# API Server runs on fixed IP
python3 sdn_api_server.py --host 192.168.1.100 --port 5000
```

Machine 2 (Web Client):
```bash
# Update js/api-client.js
const API_BASE_URL = 'http://192.168.1.100:5000';

# Run web server
python3 -m http.server 8000
```

Clients:
```
Open: http://192.168.1.200:8000
```

### Scenario 3: Docker Deployment

**Create Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000 8000

CMD ["python3", "sdn_api_server.py"]
```

**Build and Run:**
```bash
docker build -t sdn-platform .
docker run -p 5000:5000 -p 8000:8000 sdn-platform
```

### Scenario 4: Production Deployment (Gunicorn + Nginx)

**Install Production Server:**
```bash
pip install gunicorn
```

**Run with Gunicorn:**
```bash
gunicorn --worker-class eventlet -w 1 \
  --bind 0.0.0.0:5000 sdn_api_server:app
```

**Nginx Configuration:**
```nginx
upstream sdn_api {
    server localhost:5000;
}

server {
    listen 80;
    server_name sdn.example.com;

    location /api {
        proxy_pass http://sdn_api;
    }

    location / {
        alias /path/to/SDN_Website/;
    }
}
```

---

## 🔌 Custom API Endpoints

### Add New Endpoint

**Edit sdn_api_server.py:**

```python
@app.route('/api/custom/endpoint', methods=['GET', 'POST'])
def custom_endpoint():
    """Custom endpoint description"""
    if request.method == 'GET':
        return jsonify({
            'status': 'success',
            'data': network_state
        })
    
    elif request.method == 'POST':
        data = request.get_json()
        # Process data
        return jsonify({'status': 'success'})

# Emit WebSocket event
@app.route('/api/custom/event', methods=['POST'])
def trigger_custom_event():
    socketio.emit('custom_event', {
        'message': 'Custom event triggered'
    }, broadcast=True)
    return jsonify({'status': 'emitted'})
```

### Connect to Frontend

**Edit js/api-client.js:**

```javascript
// Add fetch function
async function fetchCustomData() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/custom/endpoint`);
        const data = await response.json();
        updateCustomUI(data);
    } catch (error) {
        console.error('Error fetching custom data:', error);
    }
}

// Listen for event
socket.on('custom_event', (data) => {
    console.log('Custom event received:', data);
});
```

---

## 🎨 Theming & Customization

### Colors (css/style.css)

```css
:root {
    /* Primary Colors */
    --primary-color: #3b82f6;       /* Blue */
    --secondary-color: #1e293b;     /* Dark */
    --danger-color: #ef4444;        /* Red */
    --warning-color: #f59e0b;       /* Amber */
    --success-color: #10b981;       /* Green */
    
    /* Background Colors */
    --background: #0f172a;
    --surface: #1e293b;
    --surface-light: #334155;
    
    /* Text Colors */
    --text-primary: #e2e8f0;
    --text-secondary: #94a3b8;
    
    /* Border Color */
    --border-color: #334155;
}
```

### Add Custom Theme

```css
/* In css/style.css */
:root.theme-light {
    --background: #f8fafc;
    --surface: #f1f5f9;
    --text-primary: #0f172a;
    --text-secondary: #475569;
}

/* Toggle in JavaScript */
document.documentElement.classList.toggle('theme-light');
```

---

## 📊 Data Persistence

### Option 1: SQLite Database

**Install:**
```bash
pip install flask-sqlalchemy
```

**Example:**
```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sdn.db'
db = SQLAlchemy(app)

class Threat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime)

db.create_all()
```

### Option 2: PostgreSQL

**Install:**
```bash
pip install psycopg2-binary
```

**Connection:**
```python
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://user:password@localhost/sdn_db'
```

### Option 3: File-Based

```python
import json

def save_state():
    with open('state.json', 'w') as f:
        json.dump(network_state, f)

def load_state():
    with open('state.json', 'r') as f:
        return json.load(f)
```

---

## 🔒 Security Hardening

### CORS Configuration

```python
from flask_cors import CORS

# Restrict to specific origins
CORS(app, origins=['http://localhost:8000', 'https://sdn.example.com'])
```

### Rate Limiting

```bash
pip install flask-limiter
```

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/attacks/simulate', methods=['POST'])
@limiter.limit("10 per minute")
def simulate_attack():
    # Rate limited to 10 requests per minute
    pass
```

### Authentication

```python
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if username == 'admin' and password == 'secret':
        return username

@app.route('/api/protected')
@auth.login_required
def protected():
    return {'data': 'sensitive'}
```

---

## 🧪 Testing

### Unit Tests

**Create tests/test_api.py:**

```python
import unittest
from sdn_api_server import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_health(self):
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
    
    def test_stats(self):
        response = self.app.get('/api/stats')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('throughput', data)

if __name__ == '__main__':
    unittest.main()
```

**Run Tests:**
```bash
python -m pytest tests/
```

---

## 📈 Monitoring & Logging

### Log File Configuration

```python
import logging

logging.basicConfig(
    filename='sdn_platform.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info('Application started')
logger.warning('Warning message')
logger.error('Error occurred')
```

### Performance Monitoring

```python
import time

start_time = time.time()
# Execute code
elapsed = time.time() - start_time
logger.info(f'Request took {elapsed:.3f} seconds')
```

---

## 🚨 Troubleshooting

### Common Issues

**Issue: Port Already in Use**
```bash
# Find and kill process
lsof -i :5000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

**Issue: Module Not Found**
```bash
pip install --upgrade -r requirements.txt
```

**Issue: WebSocket Connection Failed**
```javascript
// Check browser console
console.log(socket);  // Should not be null

// Enable debug logging
socket.io.reconnection = true;
socket.io.reconnectionDelay = 100;
```

**Issue: CORS Error**
```python
# Enable CORS for development
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

---

## 📚 Additional Resources

- **Flask Documentation:** https://flask.palletsprojects.com
- **Socket.IO:** https://socket.io/docs
- **WebSocket:** https://developer.mozilla.org/en-US/docs/Web/API/WebSocket
- **Python Logging:** https://docs.python.org/3/library/logging.html

---

## 🎯 Best Practices

1. **Always validate input** - Sanitize all user inputs
2. **Use HTTPS in production** - Encrypt all connections
3. **Monitor performance** - Track response times and errors
4. **Backup data regularly** - Don't lose important information
5. **Update dependencies** - Keep packages current
6. **Log everything** - Maintain audit trails
7. **Test thoroughly** - Verify all functionality
8. **Document changes** - Keep records of modifications

---

## 📞 Support

For configuration questions or issues:
1. Check the logs: `cat sdn_platform.log`
2. Check browser console: F12 → Console
3. Check server output: Look at terminal output
4. Review documentation: README.md, QUICKSTART.md
5. Test endpoints: Use curl or Postman

---

**Last Updated:** December 26, 2024  
**Version:** 1.0.0
