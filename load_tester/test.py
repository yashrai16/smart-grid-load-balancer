import requests
import threading
import time

CHARGE_REQUEST_URL = "http://charge_request_service:5000/request_charge"
NUM_REQUESTS = 50  # Total charging requests
CONCURRENCY = 10   # How many simultaneous threads

def send_request(request_id):
    try:
        response = requests.post(CHARGE_REQUEST_URL)
        print(f"[{request_id}] Status: {response.status_code}, Routed to: {response.json().get('routed_to')}")
    except Exception as e:
        print(f"[{request_id}] Failed: {e}")

def simulate_load():
    threads = []
    for i in range(NUM_REQUESTS):
        t = threading.Thread(target=send_request, args=(i,))
        threads.append(t)
        t.start()
        time.sleep(0.05)  # slight delay to simulate near-real conditions

    for t in threads:
        t.join()

if __name__ == "__main__":
    simulate_load()
