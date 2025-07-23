from flask import Flask, request, jsonify
import requests
from src.ml.threat_detector import ThreatDetector

class CoreController:
    def __init__(self):
        self.aggregation_controllers = []
        self.threat_detector = ThreatDetector()
        # Initial training data
        X_train = [[100, 10000], [200, 20000], [150, 15000]]
        self.threat_detector.train(X_train)
        self.app = Flask(__name__)
        self.app.add_url_rule('/register', 'register', self.register, methods=['POST'])
        self.app.add_url_rule('/flow_stats', 'flow_stats', self.handle_flow_stats, methods=['POST'])

    def register(self):
        data = request.get_json()
        controller_type = data.get('controller_type')
        controller_url = data.get('url')
        if controller_type == 'aggregation' and controller_url:
            self.aggregation_controllers.append(controller_url)
            return jsonify({'status': 'success'})
        return jsonify({'status': 'failure'}), 400

    def handle_flow_stats(self):
        stats = request.get_json()
        # Logic to process flow stats from aggregation controllers
        print(f"Received flow stats: {stats}")
        threat = self.threat_detector.detect(stats)
        if threat['threat'] != 'None':
            print(f"Threat detected: {threat}")
            # In a real scenario, we would send alerts to other controllers
        return jsonify({'status': 'success'})

    def get_load(self):
        # In a real scenario, this would be a more sophisticated metric
        return len(self.aggregation_controllers)

    def run(self, host, port):
        self.app.run(host=host, port=port)

if __name__ == '__main__':
    controller = CoreController()
    controller.run(host='0.0.0.0', port=5000)
