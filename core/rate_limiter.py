import time
import asyncio
from typing import Dict, Any, Optional

class TokenBucketRateLimiter:
    def __init__(self, requests_per_minute: int = 30, tokens_per_minute: int = 60000):
        self.rpm = requests_per_minute
        self.tpm = tokens_per_minute
        self.request_tokens = requests_per_minute
        self.token_tokens = tokens_per_minute
        self.last_refill = time.time()
        self.lock = asyncio.Lock()

    async def acquire(self, estimated_tokens: int = 500) -> bool:
        async with self.lock:
            now = time.time()
            elapsed = now - self.last_refill
            self.last_refill = now

            # Refill tokens based on elapsed time (60s window)
            self.request_tokens = min(self.rpm, self.request_tokens + elapsed * (self.rpm / 60.0))
            self.token_tokens = min(self.tpm, self.token_tokens + elapsed * (self.tpm / 60.0))

            if self.request_tokens >= 1 and self.token_tokens >= estimated_tokens:
                self.request_tokens -= 1
                self.token_tokens -= estimated_tokens
                return True
            return False

    async def wait_and_acquire(self, estimated_tokens: int = 500, timeout: float = 10.0):
        start = time.time()
        while time.time() - start < timeout:
            if await self.acquire(estimated_tokens):
                return True
            await asyncio.sleep(0.1)
        return False
