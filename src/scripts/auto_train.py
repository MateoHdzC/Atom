"""
ATOM Auto-Trainer
Automated pipeline: Generate data → Train → Repeat

Usage:
    python auto_train.py --rounds 5 --examples-per-round 50
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from rich.console import Console

console = Console()

def run_cmd(cmd: str, desc: str) -> bool:
    """Run command and return success."""
    console.print(f"\n[bold cyan]{desc}[/bold cyan]")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        console.print(f"[green]OK[/green]")
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[red]FAILED[/red]")
        if e.stderr:
            console.print(f"[red]{e.stderr[-200:]}[/red]")
        return False

def stop_ollama():
    """Stop Ollama to free RAM."""
    console.print("\n[yellow]Stopping Ollama...[/yellow]")
    subprocess.run("pkill -f ollama", shell=True, capture_output=True)
    time.sleep(2)
    console.print("[green]Ollama stopped[/green]")

def start_ollama():
    """Start Ollama."""
    console.print("\n[yellow]Starting Ollama...[/yellow]")
    subprocess.Popen("ollama serve", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(5)
    console.print("[green]Ollama started[/green]")

def generate_data(num_examples: int) -> bool:
    """Generate training data with teacher."""
    start_ollama()
    time.sleep(3)
    
    cmd = f"python scripts/generate_data.py --teacher chat --num-examples {num_examples}"
    success = run_cmd(cmd, f"Generating {num_examples} examples")
    
    stop_ollama()
    return success

def train_model() -> bool:
    """Train the model."""
    cmd = "python scripts/train_200m.py"
    return run_cmd(cmd, "Training 200M model")

def test_model():
    """Quick test of the model."""
    cmd = "python scripts/test_model.py --model ./models/atom-simple"
    run_cmd(cmd, "Testing model")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="ATOM Auto-Trainer")
    parser.add_argument("--rounds", type=int, default=5, help="Number of training rounds")
    parser.add_argument("--examples-per-round", type=int, default=50, help="Examples to generate per round")
    parser.add_argument("--skip-test", action="store_true", help="Skip testing after each round")
    
    args = parser.parse_args()
    
    console.print("\n[bold blue]=== ATOM Auto-Trainer ===[/bold blue]\n")
    console.print(f"[cyan]Rounds:[/cyan] {args.rounds}")
    console.print(f"[cyan]Examples per round:[/cyan] {args.examples_per_round}")
    console.print(f"[cyan]Total examples:[/cyan] {args.rounds * args.examples_per_round}")
    
    for round_num in range(1, args.rounds + 1):
        console.print(f"\n[bold yellow]=== Round {round_num}/{args.rounds} ===[/bold yellow]")
        
        # Step 1: Generate data
        console.print(f"\n[bold]Step 1: Generating data...[/bold]")
        if not generate_data(args.examples_per_round):
            console.print("[red]Data generation failed. Skipping round.[/red]")
            continue
        
        # Step 2: Train
        console.print(f"\n[bold]Step 2: Training...[/bold]")
        if not train_model():
            console.print("[red]Training failed. Skipping round.[/red]")
            continue
        
        # Step 3: Test (optional)
        if not args.skip_test:
            console.print(f"\n[bold]Step 3: Testing...[/bold]")
            test_model()
        
        console.print(f"\n[green]Round {round_num} complete![/green]")
        
        # Save checkpoint
        checkpoint_dir = f"./models/atom-simple-round-{round_num}"
        run_cmd(f"cp -r ./models/atom-simple {checkpoint_dir}", f"Saving checkpoint to {checkpoint_dir}")
    
    console.print("\n[bold green]=== Auto-Training complete! ===[/bold green]")
    console.print(f"\n[cyan]Final model:[/cyan] ./models/atom-simple")
    console.print(f"[cyan]Total examples trained:[/cyan] {args.rounds * args.examples_per_round}")

if __name__ == "__main__":
    main()
