
import os
from flask import Flask, request, jsonify
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def _authenticate(req):
    token = req.headers.get('Authorization')
    expected = os.getenv('SECRET_KEY')
    if not expected or token != f"Bearer {expected}":
        logger.warning("Unauthorized access attempt.")
        return False
    return True

@app.route('/register', methods=['POST'])
def register():
    if not _authenticate(request):
        return jsonify({'status': 'unauthorized'}), 401
    # Logic to register a new controller
    logger.info("Controller registered.")
    return jsonify({'status': 'success'})

@app.route('/unregister', methods=['POST'])
def unregister():
    if not _authenticate(request):
        return jsonify({'status': 'unauthorized'}), 401
    # Logic to unregister a controller
    logger.info("Controller unregistered.")
    return jsonify({'status': 'success'})

@app.route('/flow_stats', methods=['POST'])
def flow_stats():
    if not _authenticate(request):
        return jsonify({'status': 'unauthorized'}), 401
    # Logic to handle flow statistics
    logger.info(f"Flow stats received: {request.get_json()}")
    return jsonify({'status': 'success'})

@app.route('/threat_alert', methods=['POST'])
def threat_alert():
    if not _authenticate(request):
        return jsonify({'status': 'unauthorized'}), 401
    # Logic to handle threat alerts
    logger.info(f"Threat alert received: {request.get_json()}")
    return jsonify({'status': 'success'})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    logger.remove()
    logger.add(lambda msg: print(msg, end=''), level=log_level)
    app.run(debug=False)
