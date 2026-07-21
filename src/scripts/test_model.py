"""
ATOM Test Script
Quick test to verify the trained model works.

Usage:
    python test_model.py
    python test_model.py --model ./models/atom-1b
"""

import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, pipeline
from rich.console import Console

console = Console()

def test_model(model_path: str = "./models/atom-1b"):
    """Test the trained model with simple prompts."""
    console.print("\n[bold blue]🧪 ATOM Model Test[/bold blue]\n")
    
    # Check for GPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    console.print(f"[cyan]ℹ[/cyan] Using device: {device}")
    
    # Load model and tokenizer
    console.print(f"\n[bold]Loading model from: {model_path}[/bold]")
    
    try:
        tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        model = GPT2LMHeadModel.from_pretrained(model_path)
        console.print("[green]✓[/green] Model loaded successfully")
    except Exception as e:
        console.print(f"[red]✗[/red] Error loading model: {e}")
        console.print("\n[yellow]⚠[/yellow] Have you trained the model yet?")
        console.print("Run: python train.py")
        return
    
    # Create text generation pipeline
    generator = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device=0 if device == "cuda" else -1
    )
    
    # Test prompts
    test_prompts = [
        "Hola, ¿cómo estás?",
        "La capital de España es",
        "Python es",
        "La suma de 2 + 2 es",
    ]
    
    console.print("\n[bold]Testing model with sample prompts...[/bold]\n")
    
    for prompt in test_prompts:
        console.print(f"[cyan]Prompt:[/cyan] {prompt}")
        
        try:
            result = generator(
                prompt,
                max_new_tokens=30,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
            
            generated_text = result[0]['generated_text']
            console.print(f"[green]ATOM:[/green] {generated_text}\n")
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}\n")
    
    console.print("[bold green]✅ Test complete![/bold green]")

def chat_mode(model_path: str = "./models/atom-1b"):
    """Interactive chat mode with the model."""
    console.print("\n[bold blue]💬 ATOM Chat Mode[/bold blue]")
    console.print("Type 'exit' or 'quit' to end the conversation\n")
    
    # Load model
    try:
        tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        model = GPT2LMHeadModel.from_pretrained(model_path)
    except Exception as e:
        console.print(f"[red]✗[/red] Error loading model: {e}")
        return
    
    # Create pipeline
    device = "cuda" if torch.cuda.is_available() else "cpu"
    generator = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device=0 if device == "cuda" else -1
    )
    
    # Chat loop
    while True:
        try:
            user_input = console.input("[bold cyan]You:[/bold cyan] ")
            
            if user_input.lower() in ['exit', 'quit', 'salir']:
                console.print("\n[yellow]Goodbye![/yellow]")
                break
            
            if not user_input.strip():
                continue
            
            # Generate response
            result = generator(
                user_input,
                max_new_tokens=30,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
            
            response = result[0]['generated_text']
            # Remove the input prompt from the response
            if response.startswith(user_input):
                response = response[len(user_input):].strip()
            
            console.print(f"[bold green]ATOM:[/bold green] {response}\n")
            
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}\n")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="ATOM Model Test")
    parser.add_argument("--model", type=str, default="./models/atom-1b", help="Path to model directory")
    parser.add_argument("--chat", action="store_true", help="Start interactive chat mode")
    
    args = parser.parse_args()
    
    if args.chat:
        chat_mode(args.model)
    else:
        test_model(args.model)
