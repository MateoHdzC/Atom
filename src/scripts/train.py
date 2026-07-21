"""
ATOM Training Script
Trains a language model from scratch using HuggingFace Transformers.

Usage:
    python train.py --config config/atom-1b.yaml
    python train.py --epochs 3 --batch-size 4
"""

import os
import sys
import yaml
import torch
from pathlib import Path
from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer,
    GPT2Config,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments
)
from datasets import Dataset
from rich.console import Console

console = Console()

def load_config(config_path: str) -> dict:
    """Load training configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def create_model(config: dict) -> GPT2LMHeadModel:
    """Create a new GPT-2 model from configuration."""
    model_config = GPT2Config(
        vocab_size=config['model']['vocab_size'],
        n_positions=config['model']['n_positions'],
        n_embd=config['model']['n_embd'],
        n_layer=config['model']['n_layer'],
        n_head=config['model']['n_head']
    )
    model = GPT2LMHeadModel(model_config)
    console.print(f"[green]OK[/green] Model created: {sum(p.numel() for p in model.parameters()):,} parameters")
    return model

def load_tokenizer(config: dict) -> GPT2Tokenizer:
    """Load or create tokenizer."""
    tokenizer = GPT2Tokenizer.from_pretrained(config['tokenizer']['name'])
    # GPT-2 doesn't have a pad token by default, so we set it to eos_token
    tokenizer.pad_token = tokenizer.eos_token
    console.print(f"[green]OK[/green] Tokenizer loaded: {config['tokenizer']['name']}")
    return tokenizer

def prepare_dataset(file_path: str, tokenizer: GPT2Tokenizer, block_size: int) -> Dataset:
    """Prepare dataset for training."""
    if not os.path.exists(file_path):
        console.print(f"[yellow]WARN[/yellow] Dataset file not found: {file_path}")
        console.print("[yellow]WARN[/yellow] Creating sample dataset for testing...")
        create_sample_dataset(file_path)
    
    # Read text file
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Tokenize the entire text
    tokenized_text = tokenizer.encode(text)
    
    # Split into blocks
    examples = []
    for i in range(0, len(tokenized_text) - block_size, block_size):
        examples.append(tokenized_text[i:i + block_size])
    
    # Create dataset with proper format
    dataset = Dataset.from_dict({
        "input_ids": examples,
        "attention_mask": [[1] * len(ex) for ex in examples],
        "labels": examples
    })
    
    console.print(f"[green]OK[/green] Dataset loaded: {len(examples)} examples")
    return dataset

def create_sample_dataset(file_path: str):
    """Create a sample dataset for testing."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    sample_texts = [
        "Hola, como estas? Estoy bien, gracias por preguntar.",
        "La capital de Espana es Madrid.",
        "Python es un lenguaje de programacion popular.",
        "El sol es una estrella que esta en el centro del sistema solar.",
        "La suma de 2 + 2 es 4.",
        "Me gusta aprender cosas nuevas todos los dias.",
        "La inteligencia artificial esta cambiando el mundo.",
        "La Tierra es el tercer planeta del sistema solar.",
        "La musica es una forma de arte que utiliza el sonido.",
        "La programacion es una habilidad muy valiosa en la actualidad.",
    ] * 100  # Repeat to have enough data
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sample_texts))
    
    console.print(f"[green]OK[/green] Sample dataset created: {file_path}")

def train(config_path: str = None, epochs: int = None, batch_size: int = None):
    """Main training function."""
    console.print("\n[bold blue]ATOM Training[/bold blue]\n")
    
    # Load configuration
    if config_path:
        config = load_config(config_path)
    else:
        config = {
            'model': {
                'name': 'atom-1b',
                'vocab_size': 50257,
                'n_positions': 1024,
                'n_embd': 768,
                'n_layer': 12,
                'n_head': 12
            },
            'training': {
                'output_dir': './models/atom-1b',
                'num_train_epochs': epochs or 3,
                'per_device_train_batch_size': batch_size or 4,
                'gradient_accumulation_steps': 4,
                'learning_rate': 5.0e-5,
                'warmup_steps': 100,
                'logging_steps': 10,
                'save_steps': 500,
                'fp16': True
            },
            'data': {
                'train_file': './data/processed/train.txt',
                'block_size': 1024
            },
            'tokenizer': {
                'name': 'gpt2'
            }
        }
    
    # Check for GPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    console.print(f"[cyan]INFO[/cyan] Using device: {device}")
    
    if device == "cuda":
        console.print(f"[cyan]INFO[/cyan] GPU: {torch.cuda.get_device_name(0)}")
        console.print(f"[cyan]INFO[/cyan] GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    
    # Create model and tokenizer
    console.print("\n[bold]Creating model and tokenizer...[/bold]")
    model = create_model(config)
    tokenizer = load_tokenizer(config)
    
    # Prepare dataset
    console.print("\n[bold]Preparing dataset...[/bold]")
    train_dataset = prepare_dataset(config['data']['train_file'], tokenizer, config['data']['block_size'])
    
    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=config['training']['output_dir'],
        num_train_epochs=config['training']['num_train_epochs'],
        per_device_train_batch_size=config['training']['per_device_train_batch_size'],
        gradient_accumulation_steps=config['training']['gradient_accumulation_steps'],
        learning_rate=config['training']['learning_rate'],
        warmup_steps=config['training']['warmup_steps'],
        logging_steps=config['training']['logging_steps'],
        save_steps=config['training']['save_steps'],
        fp16=config['training']['fp16'] and device == "cuda",
        logging_dir='./logs',
        report_to="none",  # Disable wandb/tensorboard for now
        save_total_limit=2,
        remove_unused_columns=False,
    )
    
    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
    )
    
    # Start training
    console.print("\n[bold green]Starting training...[/bold green]\n")
    trainer.train()
    
    # Save model
    console.print("\n[bold]Saving model...[/bold]")
    trainer.save_model(config['training']['output_dir'])
    tokenizer.save_pretrained(config['training']['output_dir'])
    
    console.print(f"\n[bold green]Training complete![/bold green]")
    console.print(f"[cyan]INFO[/cyan] Model saved to: {config['training']['output_dir']}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="ATOM Training Script")
    parser.add_argument("--config", type=str, help="Path to config YAML file")
    parser.add_argument("--epochs", type=int, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, help="Batch size per device")
    
    args = parser.parse_args()
    
    train(
        config_path=args.config,
        epochs=args.epochs,
        batch_size=args.batch_size
    )
