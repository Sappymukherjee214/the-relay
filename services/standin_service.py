import asyncio
import time
import random
from typing import AsyncGenerator, Dict, Any, Optional
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel

class ChatCompletionRequest(BaseModel):
    model: str
    messages: list
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 512
    stream: Optional[bool] = False

app = FastAPI(title="Groq & Stand-In Model Service")

# Simple in-memory rate limiter state for simulation
DAILY_TOKENS_USED = 0
MAX_DAILY_TOKENS = 10000000

@app.post("/v1/chat/completions")
async def chat_completions(req: ChatCompletionRequest, request: Request):
    start_time = time.time()

    # Check if request specifies stand-in or if headers demand simulation
    use_standin = request.headers.get("X-Use-Standin", "false").lower() == "true"

    if use_standin:
        # Simulate latency (log-normal distribution)
        latency = max(0.1, random.lognormalvariate(mean=-0.5, sigma=0.5))
        await asyncio.sleep(latency)

        # Simulate occasional rate limit (429) or error (500) based on load / probability
        if random.random() < 0.05:
            raise HTTPException(status_code=429, detail="Rate limit exceeded (simulated)")

        ttft = latency * 0.4
        total_time = latency

        response_text = f"Stand-in response to query about {req.messages[-1]['content'][:30]}... [Attention Is All You Need, p. 3]"

        if req.stream:
            async def generate():
                yield f"data: {json.dumps({'choices': [{'delta': {'content': response_text}}]})}\n\n"
                yield "data: [DONE]\n\n"
            return generate() # simplified for FastAPI streaming response if needed

        return {
            "id": f"chatcmpl-{random.randint(10000,99999)}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": req.model,
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": response_text},
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": len(req.messages[-1]['content'].split()) * 2,
                "completion_tokens": len(response_text.split()),
                "total_tokens": len(req.messages[-1]['content'].split()) * 2 + len(response_text.split())
            },
            "x_groq": {
                "id": "req_standin",
                "usage": {"queue_time": 0.01, "prompt_time": 0.02, "completion_time": 0.05}
            }
        }
    else:
        # Real Groq API proxy placeholder or call
        # For actual tests without key, return mock real response structure
        return {
            "id": f"chatcmpl-real-{random.randint(10000,99999)}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": req.model,
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": "Real Groq response placeholder."},
                "finish_reason": "stop"
            }],
            "usage": {"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20}
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
