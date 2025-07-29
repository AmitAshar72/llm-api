from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from .generator import generate_response
from .logger import log_jsonl
from .config import settings
import logging
import time
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Depends
from cachetools import TTLCache
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)

# Caching: cache prompt->response for 5 minutes, up to 1000 entries
response_cache = TTLCache(maxsize=1000, ttl=300)

app = FastAPI(
    title="LLM API",
    description="A minimal REST API for prompt-based text generation",
    version="1.0.0"
)
app.state.limiter = limiter

class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=10000, description="The input prompt")

class GenerateResponse(BaseModel):
    response: str = Field(..., description="The generated response")

@app.post("/generate", response_model=GenerateResponse)
@limiter.limit("5/second")
async def generate(request: Request, body: GenerateRequest):
    print("[API] /generate called")
    print(f"[API] Request body: {body}")
    start_time = time.time()

    # Caching
    cache_key = body.prompt.strip()
    if cache_key in response_cache:
        print(f"[API] Cache hit for prompt: {cache_key}")
        response_text = response_cache[cache_key]
    else:
        print(f"[API] Cache miss for prompt: {cache_key}")
        response_text = await generate_response(body.prompt)
        response_cache[cache_key] = response_text
        print(f"[API] Cached response for prompt: {cache_key}")

    print(f"[API] Generated response: {response_text}")
    duration = time.time() - start_time
    print(f"[API] Duration: {duration:.3f}s")

    log_entry = {
        "timestamp": time.time(),
        "prompt": body.prompt,
        "response": response_text,
        "backend": settings.llm_backend.value,
        "duration_ms": round(duration * 1000, 2),
        "client_ip": str(request.client.host) if request.client else "unknown"
    }
    print(f"[API] Log entry: {log_entry}")
    log_jsonl(log_entry)

    return GenerateResponse(response=response_text)

@app.get("/health")
async def health_check():
    print("[API] /health called")
    return {
        "status": "healthy",
        "backend": settings.llm_backend.value,
        "timestamp": time.time()
    }

@app.get("/config")
async def get_config():
    print("[API] /config called")
    return {
        "backend": settings.llm_backend.value,
        "ollama_model": settings.ollama_model,
        "ollama_url": settings.ollama_url,
        "log_file": settings.log_file
    } 