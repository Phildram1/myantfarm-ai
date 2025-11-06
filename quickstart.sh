#!/bin/bash
# MyAntFarm.ai Quick Start Script for Linux/macOS

set -e

echo "================================"
echo "MyAntFarm.ai Quick Start"
echo "================================"
echo ""

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo "Error: Docker not found. Please install Docker Desktop."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose not found. Please install Docker Compose."
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 not found. Please install Python 3.11+."
    exit 1
fi

echo "Prerequisites satisfied"
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt
echo "Dependencies installed"
echo ""

# Build Docker containers
echo "Building Docker containers..."
docker-compose build
echo "Containers built"
echo ""

# Start Ollama
echo "Starting Ollama service..."
docker-compose up -d ollama
echo "Waiting for Ollama to be ready (60 seconds)..."
sleep 60
echo "Ollama started"
echo ""

# Pull model
echo "Downloading TinyLlama model (1GB, may take several minutes)..."
docker exec myantfarm_ollama ollama pull tinyllama
echo "Model downloaded"
echo ""

# Start services
echo "Starting copilot and multiagent services..."
docker-compose up -d copilot multiagent
echo "Waiting for services to initialize (20 seconds)..."
sleep 20
echo "Services ready"
echo ""

# Run quick test (3 trials)
echo "================================"
echo "Running Quick Test (3 trials)"
echo "================================"
echo "This will take about 5 minutes..."
echo ""

export TRIALS_PER_CONDITION=3
docker-compose up evaluator

echo ""
echo "================================"
echo "Quick Test Complete!"
echo "================================"
echo ""
echo "To run full evaluation (116 trials, 30 minutes):"
echo "  export TRIALS_PER_CONDITION=116"
echo "  docker-compose up evaluator"
echo ""
echo "To analyze results:"
echo "  docker-compose up analyzer"
echo "  python scripts/run_full_evaluation.py"
echo ""
echo "To view results:"
echo "  cat results/analysis/summary_statistics.csv"
echo ""