#!/usr/bin/env python3
"""
Enhanced SDN Management API Server
Provides real-time network data, attack simulation, and security controls
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit, disconnect
from datetime import datetime, timedelta
import random
import json
import threading
import time
from collections import defaultdict, deque
from loguru import logger

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Global state
network_state = {
    'active_switches': 12,
    'connected_hosts': 54,
    'traffic_rate': 5.3,  # Gbps
    'packet_loss': 0.12,  # %
    'cpu_usage': 65,
    'memory_usage': 52,
    'bandwidth_usage': 78,
    'storage_usage': 91,
    'active_flows': 2847,
    'new_flows_per_sec': 12.5,
    'dropped_packets': 3,
    'packets_per_sec': 15200000,
}

# Attack simulation
active_attacks = []
attack_history = deque(maxlen=100)
blocked_ips = set()
threat_alerts = deque(maxlen=50)

# Real-time metrics tracking
metrics_history = deque(maxlen=1000)
flow_table = {}
threat_log = deque(maxlen=200)

# Attack types
ATTACK_TYPES = {
    'ddos': {'severity': 'critical', 'description': 'DDoS Attack', 'impact': 'high'},
    'port_scan': {'severity': 'critical', 'description': 'Port Scan Activity', 'impact': 'medium'},
    'syn_flood': {'severity': 'critical', 'description': 'SYN Flood Attack', 'impact': 'high'},
    'brute_force': {'severity': 'high', 'description': 'Brute Force Attack', 'impact': 'medium'},
    'sql_injection': {'severity': 'high', 'description': 'SQL Injection Attempt', 'impact': 'high'},
    'malware': {'severity': 'high', 'description': 'Malware Detection', 'impact': 'high'},
    'unauthorized_access': {'severity': 'medium', 'description': 'Unauthorized Access', 'impact': 'medium'},
    'bandwidth_spike': {'severity': 'medium', 'description': 'Abnormal Bandwidth Spike', 'impact': 'low'},
    'anomalous_traffic': {'severity': 'low', 'description': 'Anomalous Traffic Pattern', 'impact': 'low'},
}

def generate_network_stats():
    """Generate realistic network statistics with variations."""
    return {
        'timestamp': datetime.now().isoformat(),
        'active_switches': max(8, network_state['active_switches'] + random.randint(-2, 2)),
        'connected_hosts': max(40, network_state['connected_hosts'] + random.randint(-5, 5)),
        'traffic_rate': max(0.5, network_state['traffic_rate'] + random.uniform(-1, 1.5)),
        'packet_loss': max(0, min(1, network_state['packet_loss'] + random.uniform(-0.05, 0.05))),
        'cpu_usage': max(0, min(100, network_state['cpu_usage'] + random.randint(-5, 5))),
        'memory_usage': max(0, min(100, network_state['memory_usage'] + random.randint(-3, 3))),
        'bandwidth_usage': max(0, min(100, network_state['bandwidth_usage'] + random.randint(-4, 4))),
        'storage_usage': max(0, min(100, network_state['storage_usage'] + random.randint(-2, 2))),
    }

def update_network_state():
    """Continuously update network state."""
    while True:
        try:
            stats = generate_network_stats()
            network_state.update(stats)
            metrics_history.append(stats)
            
            # Simulate new flows
            network_state['new_flows_per_sec'] = max(0.5, network_state.get('new_flows_per_sec', 12.5) + random.uniform(-2, 2))
            network_state['active_flows'] = max(100, network_state.get('active_flows', 2847) + random.randint(-100, 150))
            
            # Emit updates to connected clients
            socketio.emit('network_update', stats, broadcast=True)
            
            time.sleep(2)  # Update every 2 seconds
        except Exception as e:
            logger.error(f"Error updating network state: {e}")
            time.sleep(2)

# ============================================================================
# REST API ENDPOINTS
# ============================================================================

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get current network statistics."""
    return jsonify({
        'status': 'success',
        'data': network_state,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/metrics/history', methods=['GET'])
def get_metrics_history():
    """Get historical metrics."""
    limit = request.args.get('limit', default=100, type=int)
    return jsonify({
        'status': 'success',
        'data': list(metrics_history)[-limit:],
        'count': len(list(metrics_history)[-limit:])
    })

@app.route('/api/threats', methods=['GET'])
def get_threats():
    """Get current and recent threats."""
    return jsonify({
        'status': 'success',
        'active_threats': active_attacks,
        'threat_history': list(threat_log),
        'total_alerts': len(threat_log)
    })

@app.route('/api/attacks/simulate', methods=['POST'])
def simulate_attack():
    """Simulate a network attack."""
    try:
        data = request.get_json() or {}
        attack_type = data.get('type', 'ddos')
        source_ip = data.get('source_ip', f'203.0.113.{random.randint(1, 254)}')
        target = data.get('target', 'Switch-2')
        duration = data.get('duration', 300)  # seconds
        
        if attack_type not in ATTACK_TYPES:
            return jsonify({'status': 'error', 'message': 'Invalid attack type'}), 400
        
        attack_info = ATTACK_TYPES[attack_type]
        
        attack = {
            'id': len(active_attacks) + 1,
            'type': attack_type,
            'source_ip': source_ip,
            'target': target,
            'severity': attack_info['severity'],
            'description': attack_info['description'],
            'start_time': datetime.now().isoformat(),
            'end_time': (datetime.now() + timedelta(seconds=duration)).isoformat(),
            'status': 'active',
            'impact': attack_info['impact'],
        }
        
        active_attacks.append(attack)
        attack_history.append(attack)
        
        # Log threat
        threat_log.append({
            'timestamp': datetime.now().isoformat(),
            'threat_type': attack_type,
            'source': source_ip,
            'target': target,
            'severity': attack_info['severity'],
            'status': 'detected',
            'action': 'logged'
        })
        
        # Update network state (simulate attack impact)
        network_state['packet_loss'] = min(2.0, network_state.get('packet_loss', 0.12) + 0.5)
        network_state['traffic_rate'] *= 1.5
        
        # Broadcast to all clients
        socketio.emit('attack_detected', attack, broadcast=True)
        
        logger.warning(f"Attack simulated: {attack_type} from {source_ip}")
        
        return jsonify({
            'status': 'success',
            'message': f'Attack simulated: {attack_info["description"]}',
            'attack': attack
        })
    except Exception as e:
        logger.error(f"Error simulating attack: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/attacks/stop/<attack_id>', methods=['POST'])
def stop_attack(attack_id):
    """Stop an active attack simulation."""
    try:
        attack_id = int(attack_id)
        for attack in active_attacks:
            if attack['id'] == attack_id:
                attack['status'] = 'mitigated'
                attack['end_time'] = datetime.now().isoformat()
                
                # Recovery
                network_state['packet_loss'] = max(0, network_state.get('packet_loss', 1.0) - 0.5)
                network_state['traffic_rate'] = max(0.5, network_state.get('traffic_rate', 7.5) / 1.5)
                
                socketio.emit('attack_mitigated', attack, broadcast=True)
                
                logger.info(f"Attack {attack_id} stopped")
                return jsonify({'status': 'success', 'message': 'Attack stopped', 'attack': attack})
        
        return jsonify({'status': 'error', 'message': 'Attack not found'}), 404
    except Exception as e:
        logger.error(f"Error stopping attack: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/security/blocked-ips', methods=['GET', 'POST'])
def manage_blocked_ips():
    """Get or add blocked IPs."""
    if request.method == 'GET':
        return jsonify({
            'status': 'success',
            'blocked_ips': list(blocked_ips),
            'count': len(blocked_ips)
        })
    
    try:
        data = request.get_json() or {}
        ip = data.get('ip')
        action = data.get('action', 'block')  # block or unblock
        
        if not ip:
            return jsonify({'status': 'error', 'message': 'IP address required'}), 400
        
        if action == 'block':
            blocked_ips.add(ip)
            threat_log.append({
                'timestamp': datetime.now().isoformat(),
                'threat_type': 'ip_block',
                'source': ip,
                'target': 'network',
                'severity': 'info',
                'status': 'blocked',
                'action': 'blocked'
            })
            logger.warning(f"IP blocked: {ip}")
            socketio.emit('ip_blocked', {'ip': ip}, broadcast=True)
            return jsonify({'status': 'success', 'message': f'IP {ip} blocked', 'blocked_ips': list(blocked_ips)})
        
        elif action == 'unblock':
            blocked_ips.discard(ip)
            logger.info(f"IP unblocked: {ip}")
            socketio.emit('ip_unblocked', {'ip': ip}, broadcast=True)
            return jsonify({'status': 'success', 'message': f'IP {ip} unblocked', 'blocked_ips': list(blocked_ips)})
        
        else:
            return jsonify({'status': 'error', 'message': 'Invalid action'}), 400
    
    except Exception as e:
        logger.error(f"Error managing blocked IPs: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/security/threats/respond', methods=['POST'])
def respond_to_threat():
    """Respond to a threat (isolate host, block IP, etc.)."""
    try:
        data = request.get_json() or {}
        threat_id = data.get('threat_id')
        action = data.get('action')  # isolate_host, block_ip, alert, etc.
        target = data.get('target')
        
        if not threat_id or not action:
            return jsonify({'status': 'error', 'message': 'threat_id and action required'}), 400
        
        # Log the response
        response_log = {
            'timestamp': datetime.now().isoformat(),
            'threat_id': threat_id,
            'action': action,
            'target': target,
            'status': 'executed'
        }
        
        threat_log.append(response_log)
        
        # Update active attacks
        for attack in active_attacks:
            if attack['id'] == threat_id:
                if action == 'block_ip':
                    blocked_ips.add(attack['source_ip'])
                    logger.warning(f"Blocked IP: {attack['source_ip']}")
                elif action == 'isolate_host':
                    logger.warning(f"Isolated host: {target}")
                
                logger.info(f"Response to threat {threat_id}: {action}")
                break
        
        socketio.emit('threat_response', response_log, broadcast=True)
        
        return jsonify({
            'status': 'success',
            'message': f'Action executed: {action}',
            'response': response_log
        })
    
    except Exception as e:
        logger.error(f"Error responding to threat: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/network/flows', methods=['GET'])
def get_network_flows():
    """Get network flow information."""
    return jsonify({
        'status': 'success',
        'active_flows': network_state.get('active_flows', 2847),
        'flows_per_sec': network_state.get('new_flows_per_sec', 12.5),
        'total_packets': network_state.get('packets_per_sec', 15200000),
        'dropped': network_state.get('dropped_packets', 3)
    })

@app.route('/api/network/topology', methods=['GET'])
def get_topology():
    """Get network topology information."""
    return jsonify({
        'status': 'success',
        'controllers': [
            {'id': 'controller-1', 'status': 'active', 'ip': '10.0.0.5', 'uptime': '99.95%'}
        ],
        'switches': [
            {'id': 'switch-1', 'status': 'active', 'ports': 48, 'packets_per_sec': 4200000},
            {'id': 'switch-2', 'status': 'active', 'ports': 48, 'packets_per_sec': 5100000},
            {'id': 'switch-3', 'status': 'active', 'ports': 48, 'packets_per_sec': 5900000},
        ],
        'hosts': [
            {'id': 'host-a', 'ip': '192.168.1.10', 'status': 'connected'},
            {'id': 'host-b', 'ip': '192.168.2.15', 'status': 'connected'},
            {'id': 'host-c', 'ip': '192.168.3.20', 'status': 'connected'},
        ]
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'service': 'SDN Management API',
        'timestamp': datetime.now().isoformat(),
        'active_threats': len(active_attacks),
        'blocked_ips': len(blocked_ips)
    })

# ============================================================================
# WEBSOCKET EVENTS
# ============================================================================

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    logger.info(f"Client connected: {request.sid}")
    
    # Send initial state
    emit('initial_state', {
        'stats': network_state,
        'active_threats': active_attacks,
        'blocked_ips': list(blocked_ips)
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    logger.info(f"Client disconnected: {request.sid}")

@socketio.on('request_update')
def handle_update_request():
    """Send current state on request."""
    emit('network_update', network_state)
    emit('threats_update', {
        'active_threats': active_attacks,
        'threat_history': list(threat_log)
    })

# ============================================================================
# INITIALIZATION AND STARTUP
# ============================================================================

if __name__ == '__main__':
    logger.info("Starting SDN Management API Server")
    
    # Start background thread for updating network state
    update_thread = threading.Thread(target=update_network_state, daemon=True)
    update_thread.start()
    logger.info("Network state update thread started")
    
    # Start server
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
