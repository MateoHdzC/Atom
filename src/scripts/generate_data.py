"""
ATOM Data Generator
Uses teacher models to generate training data for ATOM.

Usage:
    python generate_data.py --teacher chat --num-examples 1000
    python generate_data.py --teacher code --num-examples 500
    python generate_data.py --teacher math --num-examples 500
"""

import os
import json
import requests
import time
from pathlib import Path
from rich.console import Console
from rich.progress import Progress

console = Console()

# Ollama API endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"

# Teacher model configurations
TEACHERS = {
    "chat": {
        "model": "qwen2.5:7b",
        "description": "Conversational data",
        "prompts": [
            "Generate a natural conversation between a user and an AI assistant. The user asks about everyday topics.",
            "Create a friendly chat where the user asks for advice about a personal topic.",
            "Write a conversation where the user asks the AI to explain a concept in simple terms.",
            "Generate a dialogue where the user shares their feelings and the AI responds empathetically.",
            "Create a conversation where the user asks for recommendations (books, movies, food, etc.).",
        ]
    },
    "code": {
        "model": "deepseek-coder:6.7b",
        "description": "Programming data",
        "prompts": [
            "Write a Python function that solves a common programming problem.",
            "Explain what this code does and how it works.",
            "Find and fix the bug in this code snippet.",
            "Write code to implement a simple data structure (list, stack, queue).",
            "Create a function that processes data and returns a result.",
        ]
    },
    "math": {
        "model": "qwen2.5-math:7b",
        "description": "Mathematics data",
        "prompts": [
            "Solve this math problem step by step.",
            "Explain the concept of derivatives in calculus.",
            "What is the formula for the area of a circle and why?",
            "Solve this algebraic equation and explain each step.",
            "Explain probability with a simple example.",
        ]
    }
}

def query_ollama(prompt: str, model: str, max_tokens: int = 500) -> str:
    """Query Ollama API to generate text."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": max_tokens,
            "temperature": 0.7,
            "top_p": 0.9
        }
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        console.print(f"[red]Error querying Ollama: {e}[/red]")
        return None

def generate_conversation_example(teacher_config: dict) -> dict:
    """Generate a single conversation example."""
    import random
    
    # Select a random prompt
    prompt_template = random.choice(teacher_config["prompts"])
    
    # Create a more specific prompt
    full_prompt = f"""Generate a natural conversation between a user and an AI assistant. 
Format it as:
User: [question or message]
AI: [response]

Make it realistic and helpful. Topic: {prompt_template}

Conversation:"""
    
    response = query_ollama(full_prompt, teacher_config["model"])
    
    if response:
        return {
            "type": "conversation",
            "text": response.strip(),
            "source": teacher_config["model"]
        }
    return None

def generate_qa_example(teacher_config: dict) -> dict:
    """Generate a question-answer example."""
    import random
    
    topics = [
        "general knowledge",
        "science",
        "history",
        "technology",
        "language",
        "daily life"
    ]
    
    topic = random.choice(topics)
    
    prompt = f"""Generate a question and answer about {topic}.
Format it as:
Q: [question]
A: [detailed answer]

Make the answer informative and clear.

Q&A:"""
    
    response = query_ollama(prompt, teacher_config["model"])
    
    if response:
        return {
            "type": "qa",
            "text": response.strip(),
            "source": teacher_config["model"],
            "topic": topic
        }
    return None

def generate_code_example(teacher_config: dict) -> dict:
    """Generate a code example."""
    import random
    
    languages = ["Python", "JavaScript", "Java"]
    language = random.choice(languages)
    
    problems = [
        "a function to sort a list",
        "a function to find the maximum value",
        "a function to reverse a string",
        "a function to check if a number is prime",
        "a function to calculate factorial",
        "a function to find duplicates in a list"
    ]
    
    problem = random.choice(problems)
    
    prompt = f"""Write {language} code for {problem}.
Include comments explaining the code.
Format it as:
```{language}
[code here]
```

Explanation: [brief explanation]

Code:"""
    
    response = query_ollama(prompt, teacher_config["model"])
    
    if response:
        return {
            "type": "code",
            "text": response.strip(),
            "source": teacher_config["model"],
            "language": language
        }
    return None

def generate_math_example(teacher_config: dict) -> dict:
    """Generate a math example."""
    import random
    
    topics = [
        "arithmetic",
        "algebra",
        "geometry",
        "calculus",
        "statistics"
    ]
    
    topic = random.choice(topics)
    
    prompt = f"""Generate a math problem about {topic} and solve it step by step.
Format it as:
Problem: [problem statement]
Solution:
Step 1: [step]
Step 2: [step]
...
Answer: [final answer]

Math problem:"""
    
    response = query_ollama(prompt, teacher_config["model"])
    
    if response:
        return {
            "type": "math",
            "text": response.strip(),
            "source": teacher_config["model"],
            "topic": topic
        }
    return None

def generate_dataset(teacher_type: str, num_examples: int, output_dir: str):
    """Generate a dataset using a teacher model."""
    if teacher_type not in TEACHERS:
        console.print(f"[red]Unknown teacher type: {teacher_type}[/red]")
        console.print(f"Available types: {', '.join(TEACHERS.keys())}")
        return
    
    teacher_config = TEACHERS[teacher_type]
    
    console.print(f"\n[bold blue]Generating {teacher_type} dataset[/bold blue]")
    console.print(f"[cyan]Teacher:[/cyan] {teacher_config['model']}")
    console.print(f"[cyan]Examples:[/cyan] {num_examples}")
    console.print(f"[cyan]Output:[/cyan] {output_dir}\n")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate examples
    examples = []
    failed = 0
    
    with Progress() as progress:
        task = progress.add_task(f"[cyan]Generating {teacher_type} examples...", total=num_examples)
        
        for i in range(num_examples):
            # Select generator based on teacher type
            if teacher_type == "chat":
                example = generate_conversation_example(teacher_config)
            elif teacher_type == "code":
                example = generate_code_example(teacher_config)
            elif teacher_type == "math":
                example = generate_math_example(teacher_config)
            else:
                example = generate_qa_example(teacher_config)
            
            if example:
                example["id"] = i + 1
                examples.append(example)
            else:
                failed += 1
            
            progress.update(task, advance=1)
            
            # Small delay to avoid overwhelming the API
            time.sleep(0.5)
    
    # Save dataset
    output_file = os.path.join(output_dir, f"{teacher_type}_dataset.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(examples, f, indent=2, ensure_ascii=False)
    
    console.print(f"\n[green]Dataset generated successfully![/green]")
    console.print(f"[cyan]Total examples:[/cyan] {len(examples)}")
    console.print(f"[cyan]Failed:[/cyan] {failed}")
    console.print(f"[cyan]Saved to:[/cyan] {output_file}")
    
    return examples

def prepare_for_training(examples: list, output_file: str):
    """Prepare generated examples for training."""
    console.print(f"\n[bold]Preparing data for training...[/bold]")
    
    # Extract text for training
    training_texts = []
    
    for example in examples:
        text = example.get("text", "")
        if text:
            # Clean up the text
            text = text.strip()
            if len(text) > 50:  # Only keep substantial examples
                training_texts.append(text)
    
    # Save as text file for training
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(training_texts))
    
    console.print(f"[green]Training data prepared:[/green] {len(training_texts)} examples")
    console.print(f"[cyan]Saved to:[/cyan] {output_file}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="ATOM Data Generator")
    parser.add_argument("--teacher", type=str, required=True, 
                       choices=["chat", "code", "math", "all"],
                       help="Teacher type to use")
    parser.add_argument("--num-examples", type=int, default=100,
                       help="Number of examples to generate")
    parser.add_argument("--output-dir", type=str, default="./data/raw",
                       help="Output directory for generated data")
    
    args = parser.parse_args()
    
    if args.teacher == "all":
        # Generate data from all teachers
        all_examples = []
        for teacher_type in ["chat", "code", "math"]:
            examples = generate_dataset(
                teacher_type, 
                args.num_examples // 3,  # Split evenly
                args.output_dir
            )
            if examples:
                all_examples.extend(examples)
        
        # Prepare combined training data
        if all_examples:
            prepare_for_training(all_examples, "./data/processed/train.txt")
    else:
        # Generate data from specific teacher
        examples = generate_dataset(args.teacher, args.num_examples, args.output_dir)
        
        # Prepare training data
        if examples:
            prepare_for_training(examples, f"./data/processed/{args.teacher}_train.txt")
