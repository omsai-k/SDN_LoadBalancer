

import os
from flask import Flask, request, jsonify
import requests
from ml.threat_detector import ThreatDetector
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


class CoreController:
    def __init__(self):
        self.aggregation_controllers = []
        self.threat_detector = ThreatDetector()
        # Initial training data (should be loaded from a secure source in production)
        X_train = [[100, 10000], [200, 20000], [150, 15000]]
        self.threat_detector.train(X_train)
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
        # Example: simple token-based auth (replace with real auth in production)
        token = req.headers.get('Authorization')
        expected = os.getenv('SECRET_KEY')
        if not expected or token != f"Bearer {expected}":
            logger.warning("Unauthorized access attempt.")
            return False
        return True

    def register(self):
        if not self._authenticate(request):
            return jsonify({'status': 'unauthorized'}), 401
        data = request.get_json()
        controller_type = data.get('controller_type')
        controller_url = data.get('url')
        if controller_type == 'aggregation' and controller_url:
            if controller_url not in self.aggregation_controllers:
                self.aggregation_controllers.append(controller_url)
                logger.info(f"Registered aggregation controller: {controller_url}")
            return jsonify({'status': 'success'})
        logger.error("Failed to register controller: missing or invalid data")
        return jsonify({'status': 'failure'}), 400

    def handle_flow_stats(self):
        if not self._authenticate(request):
            return jsonify({'status': 'unauthorized'}), 401
        stats = request.get_json()
        logger.info(f"Received flow stats: {stats}")
        try:
            threat = self.threat_detector.detect(stats)
            if threat['threat'] != 'None':
                logger.warning(f"Threat detected: {threat}")
                # TODO: send alerts to other controllers or external system
            return jsonify({'status': 'success', 'threat': threat})
        except Exception as e:
            logger.exception(f"Error processing flow stats: {e}")
            return jsonify({'status': 'error', 'message': str(e)}), 500

    def get_load(self):
        # In a real scenario, this would be a more sophisticated metric
        return jsonify({'load': len(self.aggregation_controllers)})

    def health(self):
        return jsonify({'status': 'ok'})

    def run(self, host, port):
        self.app.run(host=host, port=port)


if __name__ == '__main__':
    controller = CoreController()
    controller.run(host='0.0.0.0', port=5000)
