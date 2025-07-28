from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .generator import generate_response
from .logger import log_jsonl
import os

app = FastAPI()

class GenerateRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate(request: Request, body: GenerateRequest):
    prompt = body.prompt
    response_text = generate_response(prompt)
    response = {"response": response_text}
    # Log request and response
    log_jsonl({
        "prompt": prompt,
        "response": response_text,
        "client": str(request.client.host)
    })
    return JSONResponse(content=response) 