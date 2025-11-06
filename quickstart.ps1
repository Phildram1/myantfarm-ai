# MyAntFarm.ai Quick Start Script (PowerShell)
# Run this with: powershell -File quickstart.ps1

Write-Host "================================"
Write-Host "MyAntFarm.ai Quick Start"
Write-Host "================================"
Write-Host ""

# Check prerequisites
Write-Host "Checking prerequisites..."

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker not found. Please install Docker Desktop." -ForegroundColor Red
    exit 1
}

if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker Compose not found. Please install Docker Compose." -ForegroundColor Red
    exit 1
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python 3 not found. Please install Python 3.11+." -ForegroundColor Red
    exit 1
}

Write-Host "✓ Prerequisites satisfied" -ForegroundColor Green
Write-Host ""

# Install Python dependencies
Write-Host "Installing Python dependencies..."
pip install -q -r requirements.txt
Write-Host "✓ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Build Docker containers
Write-Host "Building Docker containers..."
docker-compose build
Write-Host "✓ Containers built" -ForegroundColor Green
Write-Host ""

# Start Ollama
Write-Host "Starting Ollama service..."
docker-compose up -d ollama
Write-Host "Waiting for Ollama to be ready (60 seconds)..."
Start-Sleep -Seconds 60
Write-Host "✓ Ollama started" -ForegroundColor Green
Write-Host ""

# Pull model
Write-Host "Downloading TinyLlama model (~1GB, may take several minutes)..."
docker exec myantfarm_ollama ollama pull tinyllama
Write-Host "✓ Model downloaded" -ForegroundColor Green
Write-Host ""

# Start services
Write-Host "Starting copilot and multiagent services..."
docker-compose up -d copilot multiagent
Write-Host "Waiting for services to initialize (20 seconds)..."
Start-Sleep -Seconds 20
Write-Host "✓ Services ready" -ForegroundColor Green
Write-Host ""

# Run quick test (3 trials)
Write-Host "================================"
Write-Host "Running Quick Test (3 trials)"
Write-Host "================================"
Write-Host "This will take about 5 minutes..."
Write-Host ""

$env:TRIALS_PER_CONDITION = "3"
docker-compose up evaluator

Write-Host ""
Write-Host "================================"
Write-Host "Quick Test Complete!"
Write-Host "================================"
Write-Host ""
Write-Host "To run full evaluation (116 trials, ~30 minutes):"
Write-Host "  $env:TRIALS_PER_CONDITION = '116'"
Write-Host "  docker-compose up evaluator"
Write-Host ""
Write-Host "To analyze results:"
Write-Host "  docker-compose up analyzer"
Write-Host "  python scripts/run_full_evaluation.py"
Write-Host ""
Write-Host "To view results:"
Write-Host "  cat results/analysis/summary_statistics.csv"
Write-Host ""