"""
ATOM Trainer 200M
Training script for 200M parameter model.
"""

import os
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Config
from rich.console import Console

console = Console()

def train():
    console.print("\n[bold blue]ATOM 200M Training[/bold blue]\n")
    
    # 200M parameter model
    config = GPT2Config(
        vocab_size=50257,
        n_positions=512,    # Medium context
        n_embd=640,        # Medium embedding
        n_layer=12,        # 12 layers
        n_head=10          # 10 heads
    )
    
    model = GPT2LMHeadModel(config)
    params = sum(p.numel() for p in model.parameters())
    console.print(f"[green]OK[/green] Model created: {params:,} parameters (~{params//1_000_000}M)")
    
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokenizer.pad_token = tokenizer.eos_token
    console.print(f"[green]OK[/green] Tokenizer loaded")
    
    # Load training data
    train_file = "./data/processed/chat_train.txt"
    if not os.path.exists(train_file):
        console.print("[red]ERROR[/red] Training data not found!")
        console.print("[yellow]Run: python scripts/generate_data.py --teacher chat --num-examples 50[/yellow]")
        return
    
    with open(train_file, 'r') as f:
        text = f.read()
    
    console.print(f"[green]OK[/green] Data loaded: {len(text)} chars")
    
    # Tokenize
    tokens = tokenizer.encode(text)
    console.print(f"[green]OK[/green] Tokens: {len(tokens)}")
    
    # Create training loop
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-5, weight_decay=0.01)
    model.train()
    
    # Split into chunks
    chunk_size = 256
    chunks = [tokens[i:i+chunk_size] for i in range(0, len(tokens)-chunk_size, chunk_size)]
    
    if not chunks:
        console.print("[red]ERROR[/red] Not enough tokens for training")
        return
    
    console.print(f"[green]OK[/green] Training chunks: {len(chunks)}")
    console.print("\n[bold green]Starting training...[/bold green]\n")
    
    # Training with gradient accumulation
    accumulation_steps = 4
    best_loss = float('inf')
    
    for epoch in range(5):
        total_loss = 0
        optimizer.zero_grad()
        
        for i, chunk in enumerate(chunks):
            input_ids = torch.tensor([chunk])
            
            outputs = model(input_ids, labels=input_ids)
            loss = outputs.loss / accumulation_steps
            loss.backward()
            
            if (i + 1) % accumulation_steps == 0:
                optimizer.step()
                optimizer.zero_grad()
            
            total_loss += loss.item() * accumulation_steps
            
            if (i + 1) % 10 == 0:
                console.print(f"Epoch {epoch+1}, Step {i+1}/{len(chunks)}, Loss: {loss.item() * accumulation_steps:.4f}")
        
        avg_loss = total_loss / len(chunks)
        console.print(f"[cyan]Epoch {epoch+1} complete. Avg loss: {avg_loss:.4f}[/cyan]")
        
        # Save best model
        if avg_loss < best_loss:
            best_loss = avg_loss
            output_dir = "./models/atom-200m"
            os.makedirs(output_dir, exist_ok=True)
            model.save_pretrained(output_dir)
            tokenizer.save_pretrained(output_dir)
            console.print(f"[green]Best model saved (loss: {best_loss:.4f})[/green]")
    
    console.print(f"\n[bold green]Training complete![/bold green]")
    console.print(f"[cyan]Best loss:[/cyan] {best_loss:.4f}")
    console.print(f"[cyan]Model saved to:[/cyan] ./models/atom-200m")

if __name__ == "__main__":
    train()
