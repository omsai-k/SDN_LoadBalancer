import matplotlib.pyplot as plt
import numpy as np

# 1. Packets vs. Time (Normal + DDoS)
time = np.arange(0, 60, 1)
packets = np.random.poisson(50, size=60)
packets[30:40] += np.random.poisson(200, size=10)  # Simulate DDoS spike
plt.figure(figsize=(6,4))
plt.plot(time, packets, label='Packets')
plt.axvspan(30, 40, color='red', alpha=0.2, label='DDoS Period')
plt.xlabel('Time (s)')
plt.ylabel('Packets')
plt.title('Network Packets Over Time')
plt.legend()
plt.tight_layout()
plt.savefig('SDN_Architecture/tests/packets_vs_time.png')
plt.close()

# 2. Threat Alerts Over Time
detections = np.zeros(60)
detections[32:38] = 1  # Threats detected during DDoS
plt.figure(figsize=(6,4))
plt.plot(time, detections, drawstyle='steps-post', label='Threat Detected')
plt.xlabel('Time (s)')
plt.ylabel('Threat Alert')
plt.title('Threat Alerts Over Time')
plt.tight_layout()
plt.savefig('SDN_Architecture/tests/threat_alerts.png')
plt.close()

# 3. Controller Load Distribution
controllers = ['Edge 1', 'Edge 2', 'Edge 3']
loads = [120, 80, 100]
plt.figure(figsize=(6,4))
plt.bar(controllers, loads, color=['blue','green','orange'])
plt.xlabel('Controller')
plt.ylabel('Flows Handled')
plt.title('Controller Load Distribution')
plt.tight_layout()
plt.savefig('SDN_Architecture/tests/controller_load.png')
plt.close()

# 4. Service Health Status
days = ['Mon','Tue','Wed','Thu','Fri']
services = ['Core','Aggregation','Edge']
health = np.ones((len(services), len(days)))
plt.figure(figsize=(6,4))
for i, svc in enumerate(services):
    plt.plot(days, health[i], label=svc)
plt.ylim(0.9, 1.1)
plt.ylabel('Health (1=Healthy)')
plt.title('Service Health Status Over Time')
plt.legend()
plt.tight_layout()
plt.savefig('SDN_Architecture/tests/service_health.png')
plt.close()
