"""
ATOM Auto-Trainer
Automated pipeline: Generate data → Train → Repeat

Usage:
    python auto_train.py --rounds 5 --examples-per-round 50
    python auto_train.py --rounds 15 --examples-per-round 50 --dashboard
"""

import os
import sys
import subprocess
import time
import threading
from datetime import datetime
from pathlib import Path
from rich.console import Console

console = Console()

# Dashboard status (shared with dashboard.py)
dashboard_status = {
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

def update_dashboard(key, value):
    """Update dashboard status."""
    dashboard_status[key] = value
    if key == "current_round" and dashboard_status["total_rounds"] > 0:
        dashboard_status["progress"] = int((value / dashboard_status["total_rounds"]) * 100)

def add_log(message):
    """Add a log entry."""
    dashboard_status["logs"].append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "message": message
    })
    if len(dashboard_status["logs"]) > 100:
        dashboard_status["logs"] = dashboard_status["logs"][-100:]

def run_cmd(cmd: str, desc: str) -> bool:
    """Run command and return success."""
    console.print(f"\n[bold cyan]{desc}[/bold cyan]")
    add_log(desc)
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        console.print(f"[green]OK[/green]")
        add_log(f"OK: {desc}")
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[red]FAILED[/red]")
        add_log(f"FAILED: {desc}")
        if e.stderr:
            console.print(f"[red]{e.stderr[-200:]}[/red]")
        return False

def stop_ollama():
    """Stop Ollama to free RAM."""
    console.print("\n[yellow]Stopping Ollama...[/yellow]")
    add_log("Stopping Ollama")
    subprocess.run("pkill -f ollama", shell=True, capture_output=True)
    time.sleep(2)
    console.print("[green]Ollama stopped[/green]")

def start_ollama():
    """Start Ollama."""
    console.print("\n[yellow]Starting Ollama...[/yellow]")
    add_log("Starting Ollama")
    subprocess.Popen("ollama serve", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(5)
    console.print("[green]Ollama started[/green]")

def generate_data(num_examples: int) -> bool:
    """Generate training data with teacher."""
    update_dashboard("current_step", "Generating data")
    add_log(f"Generating {num_examples} examples")
    
    start_ollama()
    time.sleep(3)
    
    cmd = f"python scripts/generate_data.py --teacher chat --num-examples {num_examples}"
    success = run_cmd(cmd, f"Generating {num_examples} examples")
    
    stop_ollama()
    return success

def train_model() -> bool:
    """Train the model."""
    update_dashboard("current_step", "Training model")
    add_log("Training 200M model")
    
    cmd = "python scripts/train_200m.py"
    return run_cmd(cmd, "Training 200M model")

def test_model():
    """Quick test of the model."""
    update_dashboard("current_step", "Testing model")
    add_log("Testing model")
    
    cmd = "python scripts/test_model.py --model ./models/atom-simple"
    run_cmd(cmd, "Testing model")

def start_dashboard(port=5000):
    """Start dashboard in a separate thread."""
    try:
        from dashboard import app, status
        # Share status with dashboard
        status.update(dashboard_status)
        
        def run():
            app.run(host='0.0.0.0', port=port, debug=False)
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        
        console.print(f"\n[bold green]Dashboard running at: http://localhost:{port}[/bold green]")
        console.print(f"[cyan]For ngrok: ngrok http {port}[/cyan]\n")
        return True
    except Exception as e:
        console.print(f"[yellow]Dashboard not available: {e}[/yellow]")
        return False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="ATOM Auto-Trainer")
    parser.add_argument("--rounds", type=int, default=5, help="Number of training rounds")
    parser.add_argument("--examples-per-round", type=int, default=50, help="Examples to generate per round")
    parser.add_argument("--skip-test", action="store_true", help="Skip testing after each round")
    parser.add_argument("--dashboard", action="store_true", help="Start web dashboard")
    parser.add_argument("--port", type=int, default=5000, help="Dashboard port")
    
    args = parser.parse_args()
    
    # Update dashboard status
    update_dashboard("running", True)
    update_dashboard("total_rounds", args.rounds)
    update_dashboard("examples_per_round", args.examples_per_round)
    update_dashboard("total_examples", args.rounds * args.examples_per_round)
    update_dashboard("start_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    console.print("\n[bold blue]=== ATOM Auto-Trainer ===[/bold blue]\n")
    console.print(f"[cyan]Rounds:[/cyan] {args.rounds}")
    console.print(f"[cyan]Examples per round:[/cyan] {args.examples_per_round}")
    console.print(f"[cyan]Total examples:[/cyan] {args.rounds * args.examples_per_round}")
    
    # Start dashboard if requested
    if args.dashboard:
        start_dashboard(args.port)
    
    add_log(f"Starting auto-training: {args.rounds} rounds, {args.examples_per_round} examples/round")
    
    for round_num in range(1, args.rounds + 1):
        console.print(f"\n[bold yellow]=== Round {round_num}/{args.rounds} ===[/bold yellow]")
        update_dashboard("current_round", round_num)
        add_log(f"Starting round {round_num}/{args.rounds}")
        
        # Step 1: Generate data
        console.print(f"\n[bold]Step 1: Generating data...[/bold]")
        if not generate_data(args.examples_per_round):
            console.print("[red]Data generation failed. Skipping round.[/red]")
            add_log(f"Round {round_num}: Data generation failed")
            continue
        
        # Step 2: Train
        console.print(f"\n[bold]Step 2: Training...[/bold]")
        if not train_model():
            console.print("[red]Training failed. Skipping round.[/red]")
            add_log(f"Round {round_num}: Training failed")
            continue
        
        # Step 3: Test (optional)
        if not args.skip_test:
            console.print(f"\n[bold]Step 3: Testing...[/bold]")
            test_model()
        
        console.print(f"\n[green]Round {round_num} complete![/green]")
        add_log(f"Round {round_num} complete")
        
        # Save checkpoint
        checkpoint_dir = f"./models/atom-simple-round-{round_num}"
        run_cmd(f"cp -r ./models/atom-simple {checkpoint_dir}", f"Saving checkpoint to {checkpoint_dir}")
    
    update_dashboard("running", False)
    update_dashboard("current_step", "Complete")
    add_log("Auto-training complete!")
    
    console.print("\n[bold green]=== Auto-Training complete! ===[/bold green]")
    console.print(f"\n[cyan]Final model:[/cyan] ./models/atom-simple")
    console.print(f"[cyan]Total examples trained:[/cyan] {args.rounds * args.examples_per_round}")

if __name__ == "__main__":
    main()
