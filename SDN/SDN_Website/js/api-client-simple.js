// Simple, working API client for Bridge API
const BRIDGE_API_URL = 'http://localhost:9000';

let usingBridgeAPI = false;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
  console.log('🚀 Initializing API client...');
  initializeBridgeAPI();
});

function initializeBridgeAPI() {
  console.log('🔗 Attempting to connect to Bridge API at', BRIDGE_API_URL);
  
  fetch(`${BRIDGE_API_URL}/api/health`)
    .then(response => response.json())
    .then(data => {
      console.log('✅ Bridge API Connected!', data);
      usingBridgeAPI = true;
      updateConnectionStatus(true, 'real');
      
      // Start fetching stats immediately
      fetchAndUpdateStats();
      
      // Then update every second
      setInterval(fetchAndUpdateStats, 1000);
    })
    .catch(error => {
      console.log('❌ Bridge API not available:', error);
      usingBridgeAPI = false;
      updateConnectionStatus(false, 'simulated');
    });
}

async function fetchAndUpdateStats() {
  if (!usingBridgeAPI) return;
  
  try {
    // Fetch load balancing status
    const response = await fetch(`${BRIDGE_API_URL}/api/load-balancing/status`);
    const data = await response.json();
    
    console.log('📊 Updated stats:', data);
    
    // Update Load Balancing page stats
    updateStat('active-load-balancers', data.active_load_balancers || 0);
    updateStat('average-utilization', ((data.average_utilization || 0).toFixed(1)) + '%');
    updateStat('average-utilization-dash', ((data.average_utilization || 0).toFixed(1)) + '%');
    updateStat('avg-response-time', (data.avg_response_time || 0) + 'ms');
    updateStat('failed-connections', data.failed_connections || 0);
    updateStat('failed-connections-dash', data.failed_connections || 0);
    updateStat('total-requests-processed', (data.total_requests || 0).toLocaleString());
    updateStat('total-requests-live', (data.total_requests || 0).toLocaleString());
    
  } catch (error) {
    console.error('Error fetching stats:', error);
  }
}

function updateStat(elementId, value) {
  const elem = document.getElementById(elementId);
  if (elem) {
    elem.textContent = value;
    console.log(`Updated ${elementId}: ${value}`);
  } else {
    console.warn(`Element not found: ${elementId}`);
  }
}

function updateConnectionStatus(connected, type = 'simulated') {
  console.log(`Connection Status: ${connected ? 'Connected' : 'Disconnected'} (${type})`);
  
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
    const typeLabel = type === 'real' ? '🔴 Real Network' : '⚪ Simulated';
    statusText.textContent = `${typeLabel} - ${connected ? 'Connected' : 'Disconnected'}`;
    console.log(`Status updated to: ${typeLabel}`);
  }
}

