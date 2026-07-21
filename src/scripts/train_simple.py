"""
ATOM Simple Trainer
Memory-efficient training for low RAM environments.
"""

import os
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Config
from rich.console import Console

console = Console()

def train():
    console.print("\n[bold blue]ATOM Simple Training[/bold blue]\n")
    
    # Use smallest model
    config = GPT2Config(
        vocab_size=50257,
        n_positions=256,  # Very small context
        n_embd=256,       # Small embedding
        n_layer=4,        # Only 4 layers
        n_head=4
    )
    
    model = GPT2LMHeadModel(config)
    params = sum(p.numel() for p in model.parameters())
    console.print(f"[green]OK[/green] Model created: {params:,} parameters")
    
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokenizer.pad_token = tokenizer.eos_token
    console.print(f"[green]OK[/green] Tokenizer loaded")
    
    # Load training data
    train_file = "./data/processed/chat_train.txt"
    if not os.path.exists(train_file):
        console.print("[yellow]WARN[/yellow] Creating sample data...")
        os.makedirs(os.path.dirname(train_file), exist_ok=True)
        with open(train_file, 'w') as f:
            f.write("Hola como estas\nEstoy bien gracias\nQue haces\nNada y tu\n")
    
    with open(train_file, 'r') as f:
        text = f.read()
    
    console.print(f"[green]OK[/green] Data loaded: {len(text)} chars")
    
    # Tokenize
    tokens = tokenizer.encode(text)
    console.print(f"[green]OK[/green] Tokens: {len(tokens)}")
    
    # Create simple training loop
    optimizer = torch.optim.Adam(model.parameters(), lr=5e-5)
    model.train()
    
    # Split into small chunks
    chunk_size = 128
    chunks = [tokens[i:i+chunk_size] for i in range(0, len(tokens)-chunk_size, chunk_size)]
    
    if not chunks:
        console.print("[red]ERROR[/red] Not enough tokens for training")
        return
    
    console.print(f"[green]OK[/green] Training chunks: {len(chunks)}")
    console.print("\n[bold green]Starting training...[/bold green]\n")
    
    for epoch in range(3):
        total_loss = 0
        for i, chunk in enumerate(chunks):
            input_ids = torch.tensor([chunk])
            
            outputs = model(input_ids, labels=input_ids)
            loss = outputs.loss
            
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            
            total_loss += loss.item()
            
            if (i + 1) % 5 == 0:
                console.print(f"Epoch {epoch+1}, Step {i+1}/{len(chunks)}, Loss: {loss.item():.4f}")
        
        avg_loss = total_loss / len(chunks)
        console.print(f"[cyan]Epoch {epoch+1} complete. Avg loss: {avg_loss:.4f}[/cyan]")
    
    # Save model
    output_dir = "./models/atom-simple"
    os.makedirs(output_dir, exist_ok=True)
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    console.print(f"\n[bold green]Training complete![/bold green]")
    console.print(f"[cyan]Model saved to: {output_dir}[/cyan]")

if __name__ == "__main__":
    train()
