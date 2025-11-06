from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import os
import logging
import asyncio
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Copilot Service")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "tinyllama")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "200"))


class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def can_attempt(self):
        if self.state == "CLOSED":
            return True
        elif self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
                return True
            return False
        else:  # HALF_OPEN
            return True
    
    def record_success(self):
        self.failure_count = 0
        self.state = "CLOSED"
    
    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logger.warning(f"Circuit breaker OPEN after {self.failure_count} failures")


circuit_breaker = CircuitBreaker()


class AnalyzeRequest(BaseModel):
    context: str


class AnalyzeResponse(BaseModel):
    summary: str
    actions: list


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "copilot",
        "circuit_breaker": circuit_breaker.state
    }


async def call_ollama_safe(prompt: str):
    if not circuit_breaker.can_attempt():
        logger.warning("Circuit breaker OPEN, returning None")
        return None
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": TEMPERATURE,
                        "num_predict": MAX_TOKENS
                    }
                }
            )
            
            if response.status_code == 200:
                circuit_breaker.record_success()
                return response.json().get("response", "")
            else:
                circuit_breaker.record_failure()
                return None
                
    except Exception as e:
        logger.error(f"Ollama call failed: {e}")
        circuit_breaker.record_failure()
        return None


@app.post("/analyze")
async def analyze_incident(request: AnalyzeRequest):
    logger.info(f"Received analyze request (circuit: {circuit_breaker.state})")
    
    prompt = f'''Analyze this incident briefly:

{request.context}

Provide:
1. One sentence summary
2. Two specific actions

Format:
SUMMARY: [sentence]
ACTIONS:
- [action 1]
- [action 2]'''

    output = await call_ollama_safe(prompt)
    
    # Always return valid response (fallback if needed)
    if not output or len(output) < 20:
        logger.info("Using fallback response")
        return {
            "summary": "Service experiencing errors requiring immediate attention",
            "actions": [
                "Rollback recent deployment",
                "Check system logs and metrics"
            ]
        }
    
    # Parse
    summary = ""
    actions = []
    
    try:
        if "SUMMARY:" in output:
            summary = output.split("SUMMARY:")[1].split("ACTIONS:")[0].strip()
        
        if "ACTIONS:" in output:
            actions_text = output.split("ACTIONS:")[1].strip()
            for line in actions_text.split("\n"):
                line = line.strip()
                if line and (line.startswith("-") or line.startswith("*")):
                    action = line.lstrip("-*").strip()
                    if len(action) > 5:
                        actions.append(action)
    except:
        pass
    
    if not summary:
        summary = "Service degradation detected"
    
    if not actions:
        actions = ["Investigate recent changes", "Review system metrics"]
    
    return {
        "summary": summary[:300],
        "actions": actions[:3]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)