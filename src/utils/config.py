"""Shared configuration management."""
import os

class Config:
    """Configuration for MyAntFarm.ai services."""
    
    # Ollama
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "tinyllama")
    
    # LLM
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    LLM_TIMEOUT = float(os.getenv("LLM_TIMEOUT", "300.0"))
    
    # Evaluation
    TRIALS_PER_CONDITION = int(os.getenv("TRIALS_PER_CONDITION", "116"))
    RANDOM_SEED = int(os.getenv("RANDOM_SEED", "42"))
    
    # Rate Limiting
    RATE_LIMIT_CALLS_PER_MIN = int(os.getenv("RATE_LIMIT_CALLS_PER_MIN", "10"))