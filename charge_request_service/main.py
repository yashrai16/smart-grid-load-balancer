from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# The load balancer URL (we'll configure this via docker-compose)
LOAD_BALANCER_URL = "http://load_balancer:5002"

@app.route('/request_charge', methods=['POST'])
def request_charge():
    try:
        # Forward the charging request to the load balancer
        response = requests.post(f"{LOAD_BALANCER_URL}/assign_substation")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
