"""
ATOM Training Pipeline
Complete pipeline: Generate data with teacher → Train ATOM

Usage:
    python pipeline.py --teacher chat --num-examples 100 --epochs 3
    python pipeline.py --teacher chat --num-examples 500 --epochs 5 --model-size 300m
    python pipeline.py --teacher all --num-examples 300 --epochs 5
"""

import os
import sys
import subprocess
from pathlib import Path
from rich.console import Console

console = Console()

# Model configurations
MODEL_CONFIGS = {
    "124m": "config/atom-1b.yaml",
    "300m": "config/atom-300m-chat.yaml",
}

def run_command(command: str, description: str) -> bool:
    """Run a shell command and return success status."""
    console.print(f"\n[bold cyan]{description}[/bold cyan]")
    console.print(f"[dim]Command: {command}[/dim]")
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True,
            capture_output=True,
            text=True
        )
        console.print(f"[green]Success![/green]")
        if result.stdout:
            console.print(result.stdout[-500:])  # Last 500 chars
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Failed![/red]")
        if e.stderr:
            console.print(f"[red]Error: {e.stderr[-500:]}[/red]")
        return False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="ATOM Training Pipeline")
    parser.add_argument("--teacher", type=str, default="chat",
                       choices=["chat", "code", "math", "all"],
                       help="Teacher type to use")
    parser.add_argument("--num-examples", type=int, default=100,
                       help="Number of examples to generate")
    parser.add_argument("--epochs", type=int, default=3,
                       help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=2,
                       help="Batch size for training")
    parser.add_argument("--model-size", type=str, default="124m",
                       choices=["124m", "300m"],
                       help="Model size to train")
    parser.add_argument("--skip-generation", action="store_true",
                       help="Skip data generation, use existing data")
    
    args = parser.parse_args()
    
    console.print("\n[bold blue]=== ATOM Training Pipeline ===[/bold blue]\n")
    console.print(f"[cyan]Teacher:[/cyan] {args.teacher}")
    console.print(f"[cyan]Model size:[/cyan] {args.model_size}")
    console.print(f"[cyan]Examples:[/cyan] {args.num_examples}")
    console.print(f"[cyan]Epochs:[/cyan] {args.epochs}")
    console.print(f"[cyan]Batch size:[/cyan] {args.batch_size}")
    
    # Get config file for model size
    config_file = MODEL_CONFIGS.get(args.model_size)
    if not config_file:
        console.print(f"[red]Unknown model size: {args.model_size}[/red]")
        return
    
    console.print(f"[cyan]Config:[/cyan] {config_file}")
    
    # Step 1: Generate data with teacher
    if not args.skip_generation:
        console.print("\n[bold yellow]Step 1: Generating training data with teacher...[/bold yellow]")
        
        generate_cmd = f"python scripts/generate_data.py --teacher {args.teacher} --num-examples {args.num_examples}"
        
        if not run_command(generate_cmd, "Generating data with teacher model"):
            console.print("[red]Data generation failed. Check if Ollama is running.[/red]")
            console.print("[yellow]Start Ollama with: ollama serve[/yellow]")
            return
    else:
        console.print("\n[yellow]Skipping data generation (using existing data)[/yellow]")
    
    # Step 2: Train ATOM
    console.print("\n[bold yellow]Step 2: Training ATOM...[/bold yellow]")
    
    # Determine training data file
    if args.teacher == "all":
        train_file = "./data/processed/train.txt"
    else:
        train_file = f"./data/processed/{args.teacher}_train.txt"
    
    # Check if training data exists
    if not os.path.exists(train_file):
        console.print(f"[red]Training data not found: {train_file}[/red]")
        console.print("[yellow]Run without --skip-generation first[/yellow]")
        return
    
    train_cmd = f"python scripts/train.py --config {config_file} --epochs {args.epochs} --batch-size {args.batch_size}"
    
    if not run_command(train_cmd, f"Training ATOM {args.model_size} model"):
        console.print("[red]Training failed.[/red]")
        return
    
    # Step 3: Test the model
    console.print("\n[bold yellow]Step 3: Testing trained model...[/bold yellow]")
    
    test_cmd = "python scripts/test_model.py"
    run_command(test_cmd, "Testing trained model")
    
    console.print("\n[bold green]=== Pipeline complete! ===[/bold green]")
    console.print("\n[cyan]Next steps:[/cyan]")
    console.print("1. Test the model: python scripts/test_model.py --chat")
    console.print("2. Generate more data: python scripts/generate_data.py --teacher all --num-examples 1000")
    console.print("3. Retrain: python pipeline.py --teacher all --num-examples 1000 --epochs 5")

if __name__ == "__main__":
    main()
