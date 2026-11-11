import os
import time
import httpx

async def list_models():
    key = os.getenv("GROQ_API_KEY")
    headers = {"Authorization": f"Bearer {key}"}
    async with httpx.AsyncClient() as client:
        res = await client.get("https://api.groq.com/openai/v1/models", headers=headers)
        print("Models Status:", res.status_code)
        print("Models Response:", res.text[:500])

if __name__ == "__main__":
    import asyncio
    asyncio.run(list_models())
