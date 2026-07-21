"""
ATOM Training Status
Shared status file for dashboard and auto-trainer.
"""

import json
import os

STATUS_FILE = "./data/training_status.json"

def get_status():
    """Get current training status."""
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r') as f:
            return json.load(f)
    return {
        "running": False,
        "current_round": 0,
        "total_rounds": 0,
        "examples_per_round": 0,
        "total_examples": 0,
        "current_step": "",
        "progress": 0,
        "loss": 0,
        "start_time": None,
        "logs": []
    }

def update_status(updates):
    """Update training status."""
    status = get_status()
    status.update(updates)
    
    # Calculate progress
    if status["total_rounds"] > 0:
        status["progress"] = int((status["current_round"] / status["total_rounds"]) * 100)
    
    os.makedirs(os.path.dirname(STATUS_FILE), exist_ok=True)
    with open(STATUS_FILE, 'w') as f:
        json.dump(status, f, indent=2)

def add_log(message):
    """Add a log entry."""
    from datetime import datetime
    status = get_status()
    status["logs"].append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "message": message
    })
    # Keep only last 100 logs
    if len(status["logs"]) > 100:
        status["logs"] = status["logs"][-100:]
    
    with open(STATUS_FILE, 'w') as f:
        json.dump(status, f, indent=2)
