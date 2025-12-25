#!/usr/bin/env python3
"""
Bridge API Server - Connects Dashboard to Real SDN Controller
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import time
import threading
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

CONTROLLER_URL = "http://localhost:5000"
BRIDGE_PORT = 9000
UPDATE_INTERVAL = 2

controller_cache = {
    'stats': {},
    'connected': False,
}

def fetch_stats():
    global controller_cache
    try:
        response = requests.get(f"{CONTROLLER_URL}/stats", timeout=2)
        if response.status_code == 200:
            controller_cache['stats'] = response.json()
            controller_cache['connected'] = True
            logger.info("✓ Stats fetched from controller")
    except Exception as e:
        controller_cache['connected'] = False
        logger.warning(f"Cannot reach controller: {e}")

def background_updater():
    while True:
        fetch_stats()
        time.sleep(UPDATE_INTERVAL)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'connected': controller_cache['connected']})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify({
        'data': controller_cache['stats'],
        'connected': controller_cache['connected']
    })

@app.route('/api/load-balancing/status', methods=['GET'])
def load_balancing():
    stats = controller_cache['stats']
    
    # Calculate average utilization from backend loads
    backend_loads = stats.get('backend_loads', {})
    backends_list = stats.get('backends', [])
    num_backends = len(backends_list)
    
    # Average load across all backends (including those with 0 load)
    total_load = sum(backend_loads.values()) if backend_loads else 0
    avg_per_backend = (total_load / num_backends) if num_backends > 0 else 0
    
    # Simple utilization: scale load to 0-100% (assuming 5000 is 100%)
    # This makes utilization proportional to actual request load
    avg_util = min(100, (avg_per_backend / 50) * 1)  # Simple scaling
    
    return jsonify({
        'active_load_balancers': num_backends,
        'average_utilization': round(avg_util, 1),
        'avg_response_time': stats.get('avg_response_time', 0),
        'failed_connections': stats.get('failed_connections', 0),
        'total_requests': stats.get('total_requests', 0),
        'backends': backends_list,
        'backend_loads': backend_loads,
        'connected': controller_cache['connected']
    })

@app.route('/api/threat-detection/status', methods=['GET'])
def threat_detection():
    stats = controller_cache['stats']
    return jsonify({
        'threat_detected': stats.get('threat_detected', False),
        'threat_level': stats.get('threat_level', 'safe'),
        'active_threats': stats.get('active_threats', 0),
        'packets_analyzed': stats.get('packets_analyzed', 0),
        'connected': controller_cache['connected']
    })

@app.route('/api/dashboard/summary', methods=['GET'])
def summary():
    stats = controller_cache['stats']
    return jsonify({
        'overview': {
            'active_connections': stats.get('active_load_balancers', 0),
            'total_traffic': stats.get('total_requests', 0),
            'threat_level': stats.get('threat_level', 'safe')
        },
        'connected': controller_cache['connected']
    })

if __name__ == '__main__':
    logger.info(f"Starting Bridge API on port {BRIDGE_PORT}")
    
    updater = threading.Thread(target=background_updater, daemon=True)
    updater.start()
    
    time.sleep(1)
    
    try:
        app.run(host='127.0.0.1', port=BRIDGE_PORT, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        logger.info("Bridge API stopped")
