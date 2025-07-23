from flask import Flask, request, jsonify
import requests
import sys

class AggregationController:
    def __init__(self, core_controller_url):
        self.core_controller_url = core_controller_url
        self.edge_controllers = []
        self.app = Flask(__name__)
        self.app.add_url_rule('/register', 'register', self.register, methods=['POST'])
        self.app.add_url_rule('/flow_stats', 'flow_stats', self.handle_flow_stats, methods=['POST'])

    def register_with_core(self, host, port):
        url = f'http://{host}:{port}'
        try:
            requests.post(f"{self.core_controller_url}/register", json={'controller_type': 'aggregation', 'url': url})
        except requests.exceptions.ConnectionError as e:
            print(f"Could not connect to core controller: {e}")
            sys.exit(1)


    def register(self):
        data = request.get_json()
        controller_type = data.get('controller_type')
        controller_url = data.get('url')
        if controller_type == 'edge' and controller_url:
            self.edge_controllers.append(controller_url)
            return jsonify({'status': 'success'})
        return jsonify({'status': 'failure'}), 400

    def handle_flow_stats(self):
        stats = request.get_json()
        # Logic to process flow stats from edge controllers
        # and forward them to the core controller
        print(f"Received flow stats: {stats}")
        requests.post(f"{self.core_controller_url}/flow_stats", json=stats)
        return jsonify({'status': 'success'})

    def get_load(self):
        # In a real scenario, this would be a more sophisticated metric
        return len(self.edge_controllers)

    def run(self, host, port):
        self.register_with_core(host, port)
        self.app.run(host=host, port=port)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python controller.py <core_controller_url>")
        sys.exit(1)
    core_controller_url = sys.argv[1]
    controller = AggregationController(core_controller_url)
    controller.run(host='0.0.0.0', port=5000)
