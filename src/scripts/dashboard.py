"""
ATOM Training Dashboard
Web interface to monitor training progress.

Usage:
    python dashboard.py
"""

import os
import json
import time
import threading
from datetime import datetime
from flask import Flask, render_template_string
from rich.console import Console

console = Console()
app = Flask(__name__)

# Training status
status = {
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

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>ATOM Training Dashboard</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #1a1a1a;
            color: #fff;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        h1 {
            color: #00ff88;
            text-align: center;
            margin-bottom: 30px;
        }
        .card {
            background: #2a2a2a;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid #3a3a3a;
        }
        .card h2 {
            color: #00ff88;
            margin-top: 0;
            font-size: 1.2em;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }
        .stat {
            background: #3a3a3a;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #00ff88;
        }
        .stat-label {
            color: #888;
            font-size: 0.9em;
        }
        .progress-bar {
            background: #3a3a3a;
            border-radius: 10px;
            height: 30px;
            margin: 10px 0;
            overflow: hidden;
        }
        .progress-fill {
            background: linear-gradient(90deg, #00ff88, #00cc66);
            height: 100%;
            border-radius: 10px;
            transition: width 0.5s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: #000;
        }
        .status {
            text-align: center;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .status-running {
            background: #00ff88;
            color: #000;
        }
        .status-stopped {
            background: #ff4444;
            color: #fff;
        }
        .logs {
            background: #1a1a1a;
            padding: 15px;
            border-radius: 8px;
            font-family: monospace;
            font-size: 0.9em;
            max-height: 300px;
            overflow-y: auto;
        }
        .log-entry {
            margin: 5px 0;
            padding: 5px;
            border-bottom: 1px solid #3a3a3a;
        }
        .log-time {
            color: #888;
        }
        .log-message {
            color: #fff;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 ATOM Training Dashboard</h1>
        
        <div class="status {{ 'status-running' if status.running else 'status-stopped' }}">
            {{ '🟢 RUNNING' if status.running else '🔴 STOPPED' }}
        </div>
        
        <div class="card">
            <h2>📊 Progress</h2>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {{ status.progress }}%">
                    {{ status.progress }}%
                </div>
            </div>
            <p style="text-align: center; color: #888;">
                Round {{ status.current_round }}/{{ status.total_rounds }}
            </p>
        </div>
        
        <div class="card">
            <h2>📈 Statistics</h2>
            <div class="stats">
                <div class="stat">
                    <div class="stat-value">{{ status.current_round }}</div>
                    <div class="stat-label">Current Round</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{{ status.total_rounds }}</div>
                    <div class="stat-label">Total Rounds</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{{ status.examples_per_round }}</div>
                    <div class="stat-label">Examples/Round</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{{ status.total_examples }}</div>
                    <div class="stat-label">Total Examples</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{{ "%.2f"|format(status.loss) }}</div>
                    <div class="stat-label">Current Loss</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{{ status.current_step }}</div>
                    <div class="stat-label">Current Step</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>⏱️ Time</h2>
            <p style="text-align: center;">
                Started: {{ status.start_time if status.start_time else 'Not started' }}
            </p>
        </div>
        
        <div class="card">
            <h2>📝 Logs</h2>
            <div class="logs">
                {% for log in status.logs[-20:] %}
                <div class="log-entry">
                    <span class="log-time">{{ log.time }}</span>
                    <span class="log-message">{{ log.message }}</span>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(HTML_TEMPLATE, status=status)

def update_status(key, value):
    """Update training status."""
    status[key] = value
    if key == "current_round" and status["total_rounds"] > 0:
        status["progress"] = int((value / status["total_rounds"]) * 100)

def add_log(message):
    """Add a log entry."""
    status["logs"].append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "message": message
    })
    # Keep only last 100 logs
    if len(status["logs"]) > 100:
        status["logs"] = status["logs"][-100:]

def run_dashboard(port=5000):
    """Run the dashboard server."""
    console.print(f"\n[bold green]Dashboard running at: http://localhost:{port}[/bold green]")
    console.print(f"[cyan]For ngrok: ngrok http {port}[/cyan]\n")
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == "__main__":
    run_dashboard()
