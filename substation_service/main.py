from flask import Flask, request, jsonify
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
import threading
import time
import random

app = Flask(__name__)

# Simulated load metric
current_load = Gauge('substation_current_load', 'Current load on the substation')

# Internal state
load_value = 0
lock = threading.Lock()

@app.route('/charge', methods=['POST'])
def charge_vehicle():
    global load_value
    with lock:
        load_value += 1
        current_load.set(load_value)
    # Simulate charging time
    time.sleep(random.uniform(1, 3))
    with lock:
        load_value -= 1
        current_load.set(load_value)
    return jsonify({"status": "charging complete"}), 200

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    current_load.set(0)
    app.run(host='0.0.0.0', port=5001)
