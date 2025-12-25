// Navigation active link
document.addEventListener('DOMContentLoaded', function() {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav-links a');
  
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath || (currentPath === '/' && href === 'index.html')) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });

  // Tab switching
  const tabButtons = document.querySelectorAll('.tab');
  tabButtons.forEach(button => {
    button.addEventListener('click', function() {
      const tabName = this.getAttribute('data-tab');
      switchTab(tabName);
    });
  });
});

function switchTab(tabName) {
  // Hide all tab contents
  const tabContents = document.querySelectorAll('.tab-content');
  tabContents.forEach(content => {
    content.classList.remove('active');
  });

  // Remove active class from all tabs
  const tabs = document.querySelectorAll('.tab');
  tabs.forEach(tab => {
    tab.classList.remove('active');
  });

  // Show selected tab content
  const selectedContent = document.getElementById(tabName);
  if (selectedContent) {
    selectedContent.classList.add('active');
  }

  // Add active class to clicked tab
  event.target.classList.add('active');
}

// Real-time data simulation
function getRandomValue(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function updateStats() {
  const statsElements = document.querySelectorAll('[data-stat]');
  statsElements.forEach(element => {
    const statType = element.getAttribute('data-stat');
    let value;
    
    switch(statType) {
      case 'active-switches':
        value = getRandomValue(8, 12);
        break;
      case 'connected-hosts':
        value = getRandomValue(45, 65);
        break;
      case 'traffic-rate':
        value = getRandomValue(2.5, 8.5);
        break;
      case 'packet-loss':
        value = (Math.random() * 0.3).toFixed(2);
        break;
      default:
        value = getRandomValue(0, 100);
    }
    
    element.textContent = value;
  });
}

// Update stats every 5 seconds
setInterval(updateStats, 5000);

// Initial stats update
updateStats();

// Draw topology canvas
function drawTopology() {
  const canvas = document.getElementById('topology-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  
  // Set canvas size
  canvas.width = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;

  // Background
  ctx.fillStyle = '#0a0e27';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Draw nodes
  const nodes = [
    { x: canvas.width / 2, y: 50, label: 'Controller', type: 'controller' },
    { x: 100, y: 200, label: 'Switch 1', type: 'switch' },
    { x: canvas.width / 2, y: 200, label: 'Switch 2', type: 'switch' },
    { x: canvas.width - 100, y: 200, label: 'Switch 3', type: 'switch' },
    { x: 100, y: 350, label: 'Host A', type: 'host' },
    { x: canvas.width / 2, y: 350, label: 'Host B', type: 'host' },
    { x: canvas.width - 100, y: 350, label: 'Host C', type: 'host' }
  ];

  // Draw connections
  ctx.strokeStyle = '#475569';
  ctx.lineWidth = 2;
  
  // Controller to switches
  nodes.slice(1, 4).forEach(node => {
    ctx.beginPath();
    ctx.moveTo(nodes[0].x, nodes[0].y);
    ctx.lineTo(node.x, node.y);
    ctx.stroke();
  });

  // Switches to hosts
  for (let i = 0; i < 3; i++) {
    ctx.beginPath();
    ctx.moveTo(nodes[i + 1].x, nodes[i + 1].y);
    ctx.lineTo(nodes[i + 4].x, nodes[i + 4].y);
    ctx.stroke();
  }

  // Draw nodes
  nodes.forEach((node, index) => {
    // Draw circle
    ctx.beginPath();
    ctx.arc(node.x, node.y, 20, 0, 2 * Math.PI);
    
    if (node.type === 'controller') {
      ctx.fillStyle = '#3b82f6';
    } else if (node.type === 'switch') {
      ctx.fillStyle = '#10b981';
    } else {
      ctx.fillStyle = '#f59e0b';
    }
    
    ctx.fill();
    ctx.strokeStyle = '#e2e8f0';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Draw label
    ctx.fillStyle = '#f1f5f9';
    ctx.font = 'bold 12px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(node.label, node.x, node.y + 35);
  });
}

// Draw topology on page load
document.addEventListener('DOMContentLoaded', function() {
  drawTopology();
  // Redraw on window resize
  window.addEventListener('resize', drawTopology);
});

// Threat detection simulation
function simulateThreatDetection() {
  const threats = document.querySelectorAll('.threat-item');
  threats.forEach(threat => {
    const randomStatus = ['Detected', 'Mitigated', 'Monitoring'][getRandomValue(0, 2)];
    const statusElement = threat.querySelector('.threat-status');
    if (statusElement) {
      statusElement.textContent = randomStatus;
      threat.classList.remove('threat-critical', 'threat-warning', 'threat-info');
      
      if (randomStatus === 'Detected') {
        threat.classList.add('threat-critical');
      } else if (randomStatus === 'Monitoring') {
        threat.classList.add('threat-warning');
      } else {
        threat.classList.add('threat-info');
      }
    }
  });
}

// Load balancer visualization
function drawLoadBalancer() {
  const balancerVisualization = document.getElementById('balancer-visualization');
  if (!balancerVisualization) return;

  const canvas = document.createElement('canvas');
  canvas.width = balancerVisualization.offsetWidth;
  canvas.height = 250;
  balancerVisualization.appendChild(canvas);

  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#1e293b';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Draw load balancer
  const centerX = canvas.width / 2;
  const centerY = canvas.height / 2;

  // Draw main circle (load balancer)
  ctx.beginPath();
  ctx.arc(centerX, centerY, 40, 0, 2 * Math.PI);
  ctx.fillStyle = '#3b82f6';
  ctx.fill();
  ctx.strokeStyle = '#e2e8f0';
  ctx.lineWidth = 2;
  ctx.stroke();

  // Draw label
  ctx.fillStyle = '#f1f5f9';
  ctx.font = 'bold 12px Arial';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('LB', centerX, centerY);

  // Draw backend servers
  const serverCount = 4;
  for (let i = 0; i < serverCount; i++) {
    const angle = (i / serverCount) * 2 * Math.PI;
    const x = centerX + Math.cos(angle) * 120;
    const y = centerY + Math.sin(angle) * 120;

    // Draw connection line
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(x, y);
    ctx.strokeStyle = '#475569';
    ctx.stroke();

    // Draw server circle
    ctx.beginPath();
    ctx.arc(x, y, 20, 0, 2 * Math.PI);
    ctx.fillStyle = '#10b981';
    ctx.fill();
    ctx.strokeStyle = '#e2e8f0';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Draw label
    ctx.fillStyle = '#f1f5f9';
    ctx.font = 'bold 11px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(`S${i + 1}`, x, y);
  }
}

document.addEventListener('DOMContentLoaded', function() {
  drawLoadBalancer();
});

// Chart simulation
function generateChartData() {
  const data = [];
  for (let i = 0; i < 12; i++) {
    data.push(getRandomValue(20, 95));
  }
  return data;
}

// Alert messages
function showAlert(message, type = 'info') {
  const alertContainer = document.createElement('div');
  alertContainer.className = `alert alert-${type}`;
  alertContainer.textContent = message;
  
  const mainContent = document.querySelector('.container');
  if (mainContent) {
    mainContent.insertBefore(alertContainer, mainContent.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
      alertContainer.remove();
    }, 5000);
  }
}

// Connection status indicator
function updateConnectionStatus() {
  const statusDots = document.querySelectorAll('.connection-dot');
  statusDots.forEach(dot => {
    const isConnected = getRandomValue(0, 10) > 1; // 90% connected
    if (isConnected) {
      dot.classList.add('connected');
      dot.classList.remove('disconnected');
    } else {
      dot.classList.add('disconnected');
      dot.classList.remove('connected');
    }
  });
}

setInterval(updateConnectionStatus, 3000);
updateConnectionStatus();

// Initialize all functionality
document.addEventListener('DOMContentLoaded', function() {
  // Update stats periodically
  updateStats();
  setInterval(updateStats, 5000);
});
