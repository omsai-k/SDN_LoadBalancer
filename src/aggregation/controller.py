
import os
from flask import Flask, request, jsonify
import requests
import sys
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

class AggregationController:
    def __init__(self, core_controller_url):
        self.core_controller_url = core_controller_url
        self.edge_controllers = []
        self.app = Flask(__name__)
        self._register_routes()
        self._setup_logging()

    def _register_routes(self):
        self.app.add_url_rule('/register', 'register', self.register, methods=['POST'])
        self.app.add_url_rule('/flow_stats', 'flow_stats', self.handle_flow_stats, methods=['POST'])
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

    def register_with_core(self, host, port):
        url = f'http://{host}:{port}'
        try:
            headers = {"Authorization": f"Bearer {os.getenv('SECRET_KEY','')}"}
            requests.post(f"{self.core_controller_url}/register", json={'controller_type': 'aggregation', 'url': url}, headers=headers)
            logger.info(f"Registered with core controller at {self.core_controller_url}")
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Could not connect to core controller: {e}")
            sys.exit(1)


    def register(self):
        if not self._authenticate(request):
            return jsonify({'status': 'unauthorized'}), 401
        data = request.get_json()
        controller_type = data.get('controller_type')
        controller_url = data.get('url')
        if controller_type == 'edge' and controller_url:
            if controller_url not in self.edge_controllers:
                self.edge_controllers.append(controller_url)
                logger.info(f"Registered edge controller: {controller_url}")
            return jsonify({'status': 'success'})
        logger.error("Failed to register edge controller: missing or invalid data")
        return jsonify({'status': 'failure'}), 400

    def handle_flow_stats(self):
        if not self._authenticate(request):
            return jsonify({'status': 'unauthorized'}), 401
        stats = request.get_json()
        logger.info(f"Received flow stats: {stats}")
        try:
            headers = {"Authorization": f"Bearer {os.getenv('SECRET_KEY','')}"}
            requests.post(f"{self.core_controller_url}/flow_stats", json=stats, headers=headers)
            return jsonify({'status': 'success'})
        except Exception as e:
            logger.exception(f"Error forwarding flow stats: {e}")
            return jsonify({'status': 'error', 'message': str(e)}), 500

    def get_load(self):
        return jsonify({'load': len(self.edge_controllers)})

    def health(self):
        return jsonify({'status': 'ok'})

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
