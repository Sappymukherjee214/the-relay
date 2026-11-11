import asyncio
import time
from typing import Dict, Any, Optional, Callable

class RequestQueue:
    def __init__(self, max_size: int = 100):
        self.queue = asyncio.PriorityQueue(maxsize=max_size)
        self.counter = 0

    async def enqueue(self, priority: int, request_data: Dict[str, Any], deadline: float) -> bool:
        try:
            self.counter += 1
            # Priority tuple: (priority_value, timestamp, counter, data, deadline)
            await self.queue.put((priority, time.time(), self.counter, request_data, deadline))
            return True
        except asyncio.QueueFull:
            return False

    async def dequeue(self, timeout: Optional[float] = None) -> Optional[Dict[str, Any]]:
        try:
            if timeout:
                item = await asyncio.wait_for(self.queue.get(), timeout=timeout)
            else:
                item = await self.queue.get()

            priority, enqueued_time, _, data, deadline = item

            # Check deadline
            if time.time() > deadline:
                # Expired in queue
                return None

            return {
                "data": data,
                "wait_time": time.time() - enqueued_time
            }
        except asyncio.TimeoutError:
            return None
