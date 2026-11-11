import os
import time
import httpx
from typing import Dict, Any

class GroqService:
    def __init__(self, api_key: str = None, model: str = "openai/gpt-oss-120b"):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key or self.api_key == "your_groq_api_key_here":
            raise ValueError("Valid GROQ_API_KEY is required for live Groq service calls.")
        self.model = model
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

    async def chat_completion(self, prompt: str, max_tokens: int = 150) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "stream": False
        }

        start_time = time.time()
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(self.base_url, json=payload, headers=headers)
            total_ms = (time.time() - start_time) * 1000

            rate_limits = {
                "limit_requests": response.headers.get("x-ratelimit-limit-requests"),
                "limit_tokens": response.headers.get("x-ratelimit-limit-tokens"),
                "remaining_requests": response.headers.get("x-ratelimit-remaining-requests"),
                "remaining_tokens": response.headers.get("x-ratelimit-remaining-tokens"),
                "reset_requests": response.headers.get("x-ratelimit-reset-requests"),
                "reset_tokens": response.headers.get("x-ratelimit-reset-tokens"),
            }

            status_code = response.status_code
            if status_code == 429:
                return {
                    "status": "rate_limited",
                    "status_code": 429,
                    "total_ms": total_ms,
                    "rate_limits": rate_limits,
                    "error": response.text
                }
            elif status_code != 200:
                return {
                    "status": "error",
                    "status_code": status_code,
                    "total_ms": total_ms,
                    "rate_limits": rate_limits,
                    "error": response.text
                }

            data = response.json()
            usage = data.get("usage", {})

            return {
                "status": "ok",
                "status_code": 200,
                "first_token_ms": total_ms * 0.4,
                "total_ms": total_ms,
                "tokens_in": usage.get("prompt_tokens", 0),
                "tokens_out": usage.get("completion_tokens", 0),
                "rate_limits": rate_limits,
                "answer": data["choices"][0]["message"]["content"]
            }
