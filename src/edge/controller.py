
import os
from flask import Flask, request, jsonify
import requests
import sys
import time
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

class EdgeController:
    def __init__(self, aggregation_controller_url):
        self.aggregation_controller_url = aggregation_controller_url
        self.app = Flask(__name__)
        self._register_routes()
        self._setup_logging()

    def _register_routes(self):
        self.app.add_url_rule('/get_load', 'get_load', self.get_load, methods=['GET'])
        self.app.add_url_rule('/health', 'health', self.health, methods=['GET'])

    def _setup_logging(self):
        log_level = os.getenv('LOG_LEVEL', 'INFO')
        logger.remove()
        logger.add(lambda msg: print(msg, end=''), level=log_level)

    def _authenticate(self, req):
        token = req.headers.get('Authorization')
        expected = os.getenv('SECRET_KEY')
        if not expected or token != f"Bearer {expected}":
            logger.warning("Unauthorized access attempt.")
            return False
        return True

    def register_with_aggregation(self, host, port):
        url = f'http://{host}:{port}'
        try:
            headers = {"Authorization": f"Bearer {os.getenv('SECRET_KEY','')}"}
            requests.post(f"{self.aggregation_controller_url}/register", json={'controller_type': 'edge', 'url': url}, headers=headers)
            logger.info(f"Registered with aggregation controller at {self.aggregation_controller_url}")
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Could not connect to aggregation controller: {e}")
            sys.exit(1)

    def send_flow_stats(self, stats):
        try:
            headers = {"Authorization": f"Bearer {os.getenv('SECRET_KEY','')}"}
            requests.post(f"{self.aggregation_controller_url}/flow_stats", json=stats, headers=headers)
            logger.info(f"Sent flow stats: {stats}")
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Could not connect to aggregation controller: {e}")


    def get_load(self):
        if not self._authenticate(request):
            return jsonify({'status': 'unauthorized'}), 401
        # In a real scenario, this would be a more sophisticated metric
        return jsonify({'load': 1})

    def handle_flow(self, flow):
        # Simple rule to drop packets from a specific source IP
        if flow['source_ip'] == '10.0.0.100':
            logger.info(f"Dropping packet from {flow['source_ip']}")
            # In a real scenario, we would install a flow rule in the switch
        else:
            stats = {'packets': 1200, 'bytes': 123456}
            self.send_flow_stats(stats)

    def health(self):
        return jsonify({'status': 'ok'})

    def run(self, host, port):
        self.register_with_aggregation(host, port)
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

        self.app.run(host=host, port=port)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python controller.py <aggregation_controller_url>")
        sys.exit(1)
    aggregation_controller_url = sys.argv[1]
    controller = EdgeController(aggregation_controller_url)
    controller.run(host='0.0.0.0', port=5000)
