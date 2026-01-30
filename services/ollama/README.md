# Ollama Service

This service provides the LLM backend using Ollama with TinyLlama (1B parameters).

## Configuration

- **Model**: tinyllama (pulled on first run)
- **Quantization**: 4-bit
- **Port**: 11434
- **Memory**: ~2GB RAM

## Usage

The Ollama service is automatically started by docker-compose. Other services (copilot, multiagent) connect to it via HTTP API at `http://ollama:11434`.

## Loading the Model
```bash
# Pull TinyLlama model (one-time, ~637MB)
docker exec -it myantfarm_ollama ollama pull tinyllama

# Verify model is loaded
docker exec -it myantfarm_ollama ollama list
```