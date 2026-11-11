import asyncio
import time
import random
from typing import Callable, Any

async def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    jitter: bool = True
) -> Any:
    retries = 0
    while True:
        try:
            return await func()
        except Exception as e:
            retries += 1
            if retries > max_retries:
                raise e

            # Exponential backoff with jitter
            delay = min(max_delay, base_delay * (2 ** (retries - 1)))
            if jitter:
                delay = delay * (0.5 + random.random())

            await asyncio.sleep(delay)
