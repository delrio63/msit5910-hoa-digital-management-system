import json
from datetime import datetime
import os

# Always load/save JSON from the project folder
DATA_FILE = os.path.join(os.path.dirname(__file__), "maintenance_data.json")

def load_requests():
    """Load maintenance requests from JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_requests(requests):
    """Save maintenance requests to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(requests, f, indent=4)

def submit_request(resident, description):
    """Resident submits a maintenance request."""
    requests = load_requests()
    request = {
        "resident": resident,
        "description": description,
        "status": "Submitted",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    requests.append(request)
    save_requests(requests)

def get_requests():
    """Return all maintenance requests."""
    return load_requests()

def update_status(index, new_status):
    """Admin/Board updates the status of a request."""
    requests = load_requests()
    requests[index]["status"] = new_status
    save_requests(requests)

