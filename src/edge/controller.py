from flask import Flask, request, jsonify
import requests
import sys
import time

class EdgeController:
    def __init__(self, aggregation_controller_url):
        self.aggregation_controller_url = aggregation_controller_url
        self.app = Flask(__name__)

    def register_with_aggregation(self, host, port):
        url = f'http://{host}:{port}'
        try:
            requests.post(f"{self.aggregation_controller_url}/register", json={'controller_type': 'edge', 'url': url})
        except requests.exceptions.ConnectionError as e:
            print(f"Could not connect to aggregation controller: {e}")
            sys.exit(1)

    def send_flow_stats(self, stats):
        try:
            requests.post(f"{self.aggregation_controller_url}/flow_stats", json=stats)
        except requests.exceptions.ConnectionError as e:
            print(f"Could not connect to aggregation controller: {e}")


    def get_load(self):
        # In a real scenario, this would be a more sophisticated metric
        return 1

    def handle_flow(self, flow):
        # Simple rule to drop packets from a specific source IP
        if flow['source_ip'] == '10.0.0.100':
            print(f"Dropping packet from {flow['source_ip']}")
            # In a real scenario, we would install a flow rule in the switch
        else:
            stats = {'packets': 1200, 'bytes': 123456}
            self.send_flow_stats(stats)

    def run(self, host, port):
        self.register_with_aggregation(host, port)
        self.app.add_url_rule('/get_load', 'get_load', self.get_load, methods=['GET'])
        # In a real scenario, this would be a loop that receives flows from the switch
        # For now, we'll just simulate a few flows
        flows = [
            {'source_ip': '10.0.0.1', 'destination_ip': '10.0.0.2'},
            {'source_ip': '10.0.0.100', 'destination_ip': '10.0.0.2'},
        ]
        for flow in flows:
            self.handle_flow(flow)
            time.sleep(1)

        self.app.run(host=host, port=port)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python controller.py <aggregation_controller_url>")
        sys.exit(1)
    aggregation_controller_url = sys.argv[1]
    controller = EdgeController(aggregation_controller_url)
    controller.run(host='0.0.0.0', port=5000)
