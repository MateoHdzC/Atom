"""
ATOM Core - Model Management
Handles loading, saving, and managing ATOM models.
"""

import os
import torch
from pathlib import Path
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from rich.console import Console

console = Console()

class AtomModel:
    """ATOM model wrapper for easy loading and inference."""
    
    def __init__(self, model_path: str = None):
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        if model_path:
            self.load(model_path)
    
    def load(self, model_path: str):
        """Load a trained model from directory."""
        console.print(f"[cyan]ℹ[/cyan] Loading model from: {model_path}")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        self.model = GPT2LMHeadModel.from_pretrained(model_path)
        self.model.to(self.device)
        
        console.print(f"[green]✓[/green] Model loaded on {self.device}")
    
    def generate(self, prompt: str, max_length: int = 100, temperature: float = 0.7) -> str:
        """Generate text from a prompt."""
        if not self.model or not self.tokenizer:
            raise RuntimeError("Model not loaded. Call load() first.")
        
        # Encode prompt
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")
        inputs = inputs.to(self.device)
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=max_length,
                temperature=temperature,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode
        generated_text = self.tokenizer.decode(outputs[0], return_skip_special_tokens=True)
        
        # Remove input prompt from output
        if generated_text.startswith(prompt):
            generated_text = generated_text[len(prompt):].strip()
        
        return generated_text
    
    def save(self, output_path: str):
        """Save the model to directory."""
        if not self.model or not self.tokenizer:
            raise RuntimeError("No model to save.")
        
        os.makedirs(output_path, exist_ok=True)
        self.model.save_pretrained(output_path)
        self.tokenizer.save_pretrained(output_path)
        
        console.print(f"[green]✓[/green] Model saved to: {output_path}")
    
    def get_info(self) -> dict:
        """Get model information."""
        if not self.model:
            return {"status": "not_loaded"}
        
        return {
            "status": "loaded",
            "device": self.device,
            "parameters": sum(p.numel() for p in self.model.parameters()),
            "vocab_size": self.tokenizer.vocab_size if self.tokenizer else None,
        }

def load_model(model_path: str) -> AtomModel:
    """Convenience function to load a model."""
    return AtomModel(model_path)
