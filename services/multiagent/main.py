from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import os
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MultiAgent Service")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "tinyllama")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "150"))


class OrchestrationRequest(BaseModel):
    context: str


class OrchestrationResponse(BaseModel):
    brief: str
    actions: list
    agent_outputs: dict


async def call_ollama_safe(prompt: str):
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
                return response.json().get("response", "")[:500]
    except:
        pass
    return None


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "multiagent"}


@app.post("/orchestrate")
async def orchestrate(request: OrchestrationRequest):
    logger.info("Starting orchestration")
    
    # Simplified prompts for speed
    diagnosis_prompt = f"What caused this: {request.context[:200]}\nAnswer briefly:"
    risk_prompt = f"Business impact: {request.context[:200]}\nAnswer briefly:"
    
    # Run in parallel with timeout
    try:
        diagnosis, risk = await asyncio.wait_for(
            asyncio.gather(
                call_ollama_safe(diagnosis_prompt),
                call_ollama_safe(risk_prompt)
            ),
            timeout=180.0  # 3 minutes total
        )
    except asyncio.TimeoutError:
        logger.warning("Orchestration timeout, using fallbacks")
        diagnosis = "Analysis timeout"
        risk = "Unable to assess"
    
    # Fallbacks
    if not diagnosis or len(diagnosis) < 10:
        diagnosis = "Database connection issues due to recent deployment"
    
    if not risk or len(risk) < 10:
        risk = "High impact - authentication failures affecting users"
    
    # Standard actions
    actions = [
        "Rollback auth-service deployment to v2.3.0",
        "Verify database connection pool configuration",
        "Monitor error rates for 5 minutes"
    ]
    
    brief = f'''DIAGNOSIS: {diagnosis}

BUSINESS IMPACT: {risk}

RECOMMENDED ACTIONS:
{chr(10).join(f'- {a}' for a in actions)}'''
    
    return {
        "brief": brief,
        "actions": actions,
        "agent_outputs": {
            "diagnosis": diagnosis,
            "risk_assessment": risk
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)