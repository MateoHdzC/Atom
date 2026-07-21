#!/bin/bash
# ATOM Auto-Training Script
# Monitors data generation and starts training automatically

DATA_FILE="./data/raw/chat_dataset.json"
TRAIN_FILE="./data/processed/chat_train.txt"
WAIT_MINUTES=30

echo "=== ATOM Auto-Training Monitor ==="
echo "Waiting for data generation to complete..."
echo ""

# Wait for data file to exist
while [ ! -f "$DATA_FILE" ]; do
    echo "[$(date +%H:%M)] Data not ready yet. Checking again in 2 minutes..."
    sleep 120
done

echo ""
echo "[$(date +%H:%M)] Data generation complete!"
echo "Waiting $WAIT_MINUTES minutes before training..."
echo ""

# Wait 30 minutes
sleep $((WAIT_MINUTES * 60))

echo "[$(date +%H:%M)] Starting training..."
echo ""

# Activate virtual environment and train
source .venv/bin/activate
python scripts/pipeline.py --teacher chat --num-examples 500 --epochs 5 --model-size 300m --skip-generation

echo ""
echo "[$(date +%H:%M)] Training complete!"
