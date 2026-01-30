"""Common LLM interface wrapper for all services."""
import httpx
from typing import Optional

class LLMInterface:
    """Shared LLM client for Ollama."""
    
    def __init__(self, base_url: str = "http://ollama:11434"):
        self.base_url = base_url
    
    async def generate(
        self, 
        model: str, 
        prompt: str, 
        temperature: float = 0.7,
        timeout: float = 300.0
    ) -> dict:
        """Generate completion from Ollama."""
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "temperature": temperature,
                    "stream": False
                }
            )
            return response.json()