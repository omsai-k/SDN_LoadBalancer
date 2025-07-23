import requests
import time

def simulate():
    # Simulate user traffic
    for i in range(10):
        requests.get("http://localhost:5002/get_load")
        time.sleep(1)

    # Simulate a DDoS attack
    for i in range(100):
        requests.post("http://localhost:5001/flow_stats", json={'packets': 10000, 'bytes': 1000000})
        time.sleep(0.1)

if __name__ == "__main__":
    simulate()
