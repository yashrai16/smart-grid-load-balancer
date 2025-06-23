from flask import Flask, jsonify
import requests
import re
import os

app = Flask(__name__)

# Substation instances (set in docker-compose)
SUBSTATION_HOSTS = os.environ.get("SUBSTATION_HOSTS", "substation1,substation2,substation3").split(",")
SUBSTATION_PORT = 5001

METRIC_NAME = "substation_current_load"

def get_current_load(substation_host):
    try:
        response = requests.get(f"http://{substation_host}:{SUBSTATION_PORT}/metrics")
        match = re.search(rf'{METRIC_NAME} (\d+)', response.text)
        return int(match.group(1)) if match else float('inf')
    except Exception:
        return float('inf')

@app.route('/assign_substation', methods=['POST'])
def assign_substation():
    best_substation = None
    lowest_load = float('inf')

    for host in SUBSTATION_HOSTS:
        load = get_current_load(host)
        if load < lowest_load:
            lowest_load = load
            best_substation = host

    if best_substation:
        try:
            response = requests.post(f"http://{best_substation}:{SUBSTATION_PORT}/charge")
            return jsonify({"routed_to": best_substation, "response": response.json()}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "No available substations"}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
