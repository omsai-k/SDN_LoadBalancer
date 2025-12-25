// ============================================================================
// REAL-TIME SDN MANAGEMENT API CLIENT
// ============================================================================

// Support for both real controller and bridge API
const BRIDGE_API_URL = 'http://localhost:9000';  // Bridge to real controller
const API_BASE_URL = 'http://localhost:5000';     // Fallback to simulated API
let socket = null;
let isConnected = false;
let usingBridgeAPI = false;

// Initialize WebSocket connection
function initializeWebSocket() {
  try {
    // Use socketio-client if available, otherwise fallback to polling
    if (typeof io !== 'undefined') {
      socket = io(API_BASE_URL, {
        reconnection: true,
        reconnectionDelay: 1000,
        reconnectionDelayMax: 5000,
        reconnectionAttempts: 5
      });

      socket.on('connect', () => {
        console.log('WebSocket connected');
        isConnected = true;
        updateConnectionStatus(true);
      });

      socket.on('disconnect', () => {
        console.log('WebSocket disconnected');
        isConnected = false;
        updateConnectionStatus(false);
      });

      socket.on('network_update', (data) => {
        updateDashboardStats(data);
      });

      socket.on('attack_detected', (attack) => {
        addThreatAlert(attack);
        showNotification(`⚠️ Attack Detected: ${attack.description}`, 'warning');
      });

      socket.on('attack_mitigated', (attack) => {
        showNotification(`✅ Attack Mitigated: ${attack.description}`, 'success');
        removeThreatAlert(attack.id);
      });

      socket.on('ip_blocked', (data) => {
        addBlockedIP(data.ip);
        showNotification(`🚫 IP Blocked: ${data.ip}`, 'info');
      });

      socket.on('ip_unblocked', (data) => {
        removeBlockedIP(data.ip);
        showNotification(`✅ IP Unblocked: ${data.ip}`, 'info');
      });

      socket.on('threat_response', (response) => {
        console.log('Threat response:', response);
      });
    }
  } catch (error) {
    console.warn('WebSocket not available, using polling:', error);
    // Fallback to polling
    startPolling();
  }
}

// Polling fallback for updates
function startPolling() {
  setInterval(fetchStats, 2000);
  setInterval(fetchThreats, 3000);
}

// ============================================================================
// API FETCH FUNCTIONS
// ============================================================================

// Try to connect to Bridge API (real controller)
function initializeBridgeAPI() {
  try {
    fetch(`${BRIDGE_API_URL}/api/health`)
      .then(r => r.json())
      .then(data => {
        if (data.status === 'ok') {
          usingBridgeAPI = true;
          console.log('✅ Connected to Bridge API (Real Controller)');
          updateConnectionStatus(true, 'real');
          // Start fetching from bridge API
          setInterval(fetchStatsFromBridge, 1000);
        }
      })
      .catch(() => {
        console.log('ℹ️  Bridge API not available, using simulated data');
        usingBridgeAPI = false;
        setInterval(fetchStats, 2000);
      });
  } catch (e) {
    console.log('ℹ️  Using simulated API');
    usingBridgeAPI = false;
  }
}

// Fetch stats from Bridge API (real controller data)
async function fetchStatsFromBridge() {
  try {
    const response = await fetch(`${BRIDGE_API_URL}/api/stats`);
    const data = await response.json();
    if (data.status === 'success') {
      updateDashboardStats(data.data);
      
      // Also fetch load balancing status
      fetch(`${BRIDGE_API_URL}/api/load-balancing/status`)
        .then(r => r.json())
        .then(d => {
          if (d.status === 'success') {
            updateLoadBalancingUI(d);
          }
        });
      
      // Fetch threat detection
      fetch(`${BRIDGE_API_URL}/api/threat-detection/status`)
        .then(r => r.json())
        .then(d => {
          if (d.status === 'success') {
            updateThreatDetectionUI(d);
          }
        });
    }
  } catch (error) {
    console.error('Error fetching from bridge:', error);
  }
}

async function fetchStats() {
  try {
    // Try bridge API first
    if (!usingBridgeAPI) {
      try {
        const response = await fetch(`${BRIDGE_API_URL}/api/stats`);
        if (response.ok) {
          const data = await response.json();
          if (data.status === 'success') {
            usingBridgeAPI = true;
            updateDashboardStats(data.data);
            return;
          }
        }
      } catch (e) {
        // Fall through to simulated API
      }
    }
    
    // Fallback to simulated API
    const response = await fetch(`${API_BASE_URL}/api/stats`);
    const data = await response.json();
    if (data.status === 'success') {
      updateDashboardStats(data.data);
    }
  } catch (error) {
    console.error('Error fetching stats:', error);
  }
}

async function fetchThreats() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/threats`);
    const data = await response.json();
    if (data.status === 'success') {
      updateThreatsDisplay(data.active_threats, data.threat_history);
    }
  } catch (error) {
    console.error('Error fetching threats:', error);
  }
}

async function fetchBlockedIPs() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/security/blocked-ips`);
    const data = await response.json();
    if (data.status === 'success') {
      updateBlockedIPsList(data.blocked_ips);
    }
  } catch (error) {
    console.error('Error fetching blocked IPs:', error);
  }
}

// ============================================================================
// ATTACK SIMULATION
// ============================================================================

async function simulateAttack(attackType, sourceIP, target, duration) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/attacks/simulate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        type: attackType,
        source_ip: sourceIP,
        target: target,
        duration: duration
      })
    });

    const data = await response.json();
    if (data.status === 'success') {
      console.log('Attack simulated:', data.attack);
      return data.attack;
    } else {
      showNotification('❌ Failed to simulate attack', 'error');
    }
  } catch (error) {
    console.error('Error simulating attack:', error);
    showNotification('❌ Error simulating attack', 'error');
  }
}

async function stopAttack(attackId) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/attacks/stop/${attackId}`, {
      method: 'POST'
    });

    const data = await response.json();
    if (data.status === 'success') {
      console.log('Attack stopped:', data.attack);
      return data.attack;
    }
  } catch (error) {
    console.error('Error stopping attack:', error);
  }
}

// ============================================================================
// IP BLOCKING
// ============================================================================

async function blockIP(ip) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/security/blocked-ips`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ip: ip,
        action: 'block'
      })
    });

    const data = await response.json();
    if (data.status === 'success') {
      console.log('IP blocked:', ip);
      return true;
    }
  } catch (error) {
    console.error('Error blocking IP:', error);
  }
}

async function unblockIP(ip) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/security/blocked-ips`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ip: ip,
        action: 'unblock'
      })
    });

    const data = await response.json();
    if (data.status === 'success') {
      console.log('IP unblocked:', ip);
      return true;
    }
  } catch (error) {
    console.error('Error unblocking IP:', error);
  }
}

// ============================================================================
// THREAT RESPONSE
// ============================================================================

async function respondToThreat(threatId, action, target) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/security/threats/respond`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        threat_id: threatId,
        action: action,
        target: target
      })
    });

    const data = await response.json();
    if (data.status === 'success') {
      console.log('Threat response:', data.response);
      return true;
    }
  } catch (error) {
    console.error('Error responding to threat:', error);
  }
}

// ============================================================================
// UI UPDATE FUNCTIONS
// ============================================================================

function updateDashboardStats(stats) {
  // Update stat cards
  const elements = {
    'active-switches': Math.round(stats.active_switches),
    'connected-hosts': Math.round(stats.connected_hosts),
    'traffic-rate': stats.traffic_rate.toFixed(1),
    'packet-loss': stats.packet_loss.toFixed(2),
    'cpu-usage': Math.round(stats.cpu_usage),
    'memory-usage': Math.round(stats.memory_usage),
    'bandwidth-usage': Math.round(stats.bandwidth_usage),
    'storage-usage': Math.round(stats.storage_usage),
  };

  for (const [id, value] of Object.entries(elements)) {
    const element = document.getElementById(id);
    if (element) {
      if (id.includes('usage')) {
        element.textContent = `${value}%`;
        // Update progress bar if exists
        const progressBar = element.closest('.form-group')?.querySelector('div[style*="background-color"]');
        if (progressBar) {
          progressBar.style.width = `${value}%`;
        }
      } else if (id === 'traffic-rate') {
        element.textContent = `${value} Gbps`;
      } else {
        element.textContent = value;
      }
    }
  }

  // Update progress bars
  updateProgressBar('cpu-progress', stats.cpu_usage);
  updateProgressBar('memory-progress', stats.memory_usage);
  updateProgressBar('bandwidth-progress', stats.bandwidth_usage);
  updateProgressBar('storage-progress', stats.storage_usage);
}

function updateProgressBar(id, value) {
  const bar = document.getElementById(id);
  if (bar) {
    bar.style.width = `${Math.min(value, 100)}%`;
  }
}

function updateConnectionStatus(connected) {
  const dot = document.querySelector('.connection-dot');
  if (dot) {
    if (connected) {
      dot.classList.add('connected');
      dot.classList.remove('disconnected');
    } else {
      dot.classList.add('disconnected');
      dot.classList.remove('connected');
    }
  }
}

function updateThreatsDisplay(activeThreats, threatHistory) {
  // Clear existing threats (except header)
  const threatContainer = document.querySelector('.threat-list');
  if (threatContainer) {
    threatContainer.innerHTML = '';
    activeThreats.forEach(threat => addThreatAlert(threat));
  }
}

function addThreatAlert(threat) {
  const container = document.querySelector('.threat-list') || document.querySelector('.card');
  if (!container) return;

  const threatHtml = `
    <div class="threat-item threat-${threat.severity}" data-threat-id="${threat.id}">
      <div class="threat-header">
        <div class="threat-name">🚨 ${threat.description}</div>
        <span class="threat-status status-${threat.status}">${threat.status.toUpperCase()}</span>
      </div>
      <div class="threat-details">
        <strong>Severity:</strong> ${threat.severity} | 
        <strong>Source:</strong> ${threat.source_ip} | 
        <strong>Target:</strong> ${threat.target} | 
        <strong>Impact:</strong> ${threat.impact}
      </div>
      <div style="margin-top: 0.75rem; display: flex; gap: 0.5rem;">
        <button onclick="respondToThreat(${threat.id}, 'block_ip', '${threat.source_ip}')" class="btn btn-primary" style="padding: 0.4rem 0.8rem; font-size: 0.85rem;">
          Block IP
        </button>
        <button onclick="respondToThreat(${threat.id}, 'isolate_host', '${threat.target}')" class="btn btn-primary" style="padding: 0.4rem 0.8rem; font-size: 0.85rem;">
          Isolate
        </button>
        <button onclick="stopAttack(${threat.id})" class="btn btn-secondary" style="padding: 0.4rem 0.8rem; font-size: 0.85rem;">
          Stop
        </button>
      </div>
    </div>
  `;

  if (container.querySelector('.threat-list')) {
    container.querySelector('.threat-list').insertAdjacentHTML('beforeend', threatHtml);
  } else {
    container.insertAdjacentHTML('beforeend', threatHtml);
  }
}

function removeThreatAlert(threatId) {
  const element = document.querySelector(`[data-threat-id="${threatId}"]`);
  if (element) {
    element.remove();
  }
}

function updateBlockedIPsList(ips) {
  const container = document.getElementById('blocked-ips-list');
  if (container) {
    container.innerHTML = '';
    ips.forEach(ip => {
      const html = `
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem; background-color: var(--surface-light); border-radius: 0.25rem; margin-bottom: 0.5rem;">
          <span>${ip}</span>
          <button onclick="unblockIP('${ip}')" class="btn btn-secondary" style="padding: 0.25rem 0.5rem; font-size: 0.8rem;">Unblock</button>
        </div>
      `;
      container.insertAdjacentHTML('beforeend', html);
    });
  }
}

function addBlockedIP(ip) {
  const container = document.getElementById('blocked-ips-list');
  if (container) {
    const html = `
      <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem; background-color: var(--surface-light); border-radius: 0.25rem; margin-bottom: 0.5rem;">
        <span>${ip}</span>
        <button onclick="unblockIP('${ip}')" class="btn btn-secondary" style="padding: 0.25rem 0.5rem; font-size: 0.8rem;">Unblock</button>
      </div>
    `;
    container.insertAdjacentHTML('afterbegin', html);
  }
}

function removeBlockedIP(ip) {
  const container = document.getElementById('blocked-ips-list');
  if (container) {
    const items = container.querySelectorAll('div');
    items.forEach(item => {
      if (item.textContent.includes(ip)) {
        item.remove();
      }
    });
  }
}

// ============================================================================
// NOTIFICATION SYSTEM
// ============================================================================

function showNotification(message, type = 'info') {
  const container = document.querySelector('.container');
  if (!container) return;

  const alertHtml = `
    <div class="alert alert-${type}" style="margin-bottom: 1.5rem; animation: slideIn 0.3s ease;">
      ${message}
    </div>
  `;

  container.insertAdjacentHTML('afterbegin', alertHtml);

  // Auto-remove after 5 seconds
  setTimeout(() => {
    const alert = container.querySelector('.alert');
    if (alert) alert.remove();
  }, 5000);
}

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
  console.log('Initializing real-time SDN dashboard');

  // Initialize WebSocket and polling
  initializeWebSocket();

  // Initial fetch
  fetchStats();
  fetchThreats();
  fetchBlockedIPs();

  // Add real-time update styles if not present
  if (!document.getElementById('realtime-styles')) {
    const style = document.createElement('style');
    style.id = 'realtime-styles';
    style.textContent = `
      @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
      }

      .threat-critical {
        border-left-color: var(--danger-color) !important;
      }

      .threat-high {
        border-left-color: var(--warning-color) !important;
      }

// ============================================================================
// UI UPDATE FUNCTIONS FOR REAL CONTROLLER DATA
// ============================================================================

function updateLoadBalancingUI(data) {
  // Update load balancing page with real data
  const elements = {
    'active-load-balancers': data.active_load_balancers,
    'average-utilization': data.average_utilization + '%',
    'avg-response-time': data.avg_response_time + 'ms',
    'failed-connections': data.failed_connections,
    'total-requests-processed': data.total_requests
  };
  
  for (const [id, value] of Object.entries(elements)) {
    const elem = document.getElementById(id);
    if (elem) {
      elem.textContent = value;
    }
  }
  
  // Update backend info
  if (data.backends && data.backends.length > 0) {
    const backendList = document.getElementById('backend-list');
    if (backendList) {
      backendList.innerHTML = data.backends.map(b => `
        <div class="backend-item">
          <strong>${b.name || b}</strong>: ${b.load || 0}% load
        </div>
      `).join('');
    }
  }
}

function updateThreatDetectionUI(data) {
  // Update threat detection page with real data
  const threatStatus = document.getElementById('threat-status');
  if (threatStatus) {
    threatStatus.innerHTML = `
      <div class="status-indicator ${data.threat_detected ? 'detected' : 'safe'}">
        ${data.threat_detected ? '🚨' : '✅'} ${data.threat_level.toUpperCase()}
      </div>
      <div>Active Threats: ${data.active_threats}</div>
      <div>Packets: ${data.packets_analyzed}</div>
      <div>Bytes: ${data.bytes_analyzed}</div>
    `;
  }
}

function updateConnectionStatus(connected, type = 'simulated') {
  const statusEl = document.querySelector('.connection-dot');
  const statusText = document.querySelector('.connection-status');
  
  if (statusEl) {
    if (connected) {
      statusEl.classList.add('connected');
      statusEl.classList.remove('disconnected');
    } else {
      statusEl.classList.remove('connected');
      statusEl.classList.add('disconnected');
    }
  }
  
  if (statusText) {
    const typeLabel = type === 'real' ? '(Real Network)' : '(Simulated)';
    statusText.textContent = `Status: ${connected ? 'Connected' : 'Disconnected'} ${typeLabel}`;
  }
}

// ============================================================================
// INITIALIZATION WITH BRIDGE API SUPPORT
// ============================================================================

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
  console.log('Initializing API client...');
  
  // Try bridge API first (real controller)
  initializeBridgeAPI();
  
  // Fallback to simulated API after 3 seconds
  setTimeout(() => {
    if (!usingBridgeAPI) {
      console.log('Starting simulated API...');
      initializeWebSocket();
      setInterval(fetchStats, 2000);
      setInterval(fetchThreats, 5000);
      setInterval(fetchBlockedIPs, 5000);
    }
  }, 3000);
});

      .threat-medium {
        border-left-color: var(--warning-color) !important;
      }

      .threat-low {
        border-left-color: var(--secondary-color) !important;
      }

      .status-active { background-color: #10b981; }
      .status-detected { background-color: #ef4444; }
      .status-mitigated { background-color: #10b981; }
      .status-blocked { background-color: #6366f1; }
    `;
    document.head.appendChild(style);
  }
});
