import pytest
import os
from pathlib import Path
from core.pipeline import Pipeline
from core.rate_limiter import TokenBucketRateLimiter
from core.request_queue import RequestQueue
from retrieval.bm25_retriever import BM25Retriever

def test_pipeline_understanding():
    p = Pipeline()
    res = p.stage1_understanding("What is multi-head attention?")
    assert res["intent"] == "RETRIEVAL_REQUIRED"

def test_pipeline_run():
    p = Pipeline()
    res = p.run("What is attention?")
    assert "answer" in res
    assert len(res["citations"]) > 0

def test_retriever_from_outside_root(monkeypatch, tmp_path):
    # Change current working directory to a temporary directory outside repo root
    monkeypatch.chdir(tmp_path)
    retriever = BM25Retriever()
    results = retriever.retrieve("attention", top_k=1)
    assert len(results) > 0
    assert "paper_title" in results[0]

@pytest.mark.asyncio
async def test_rate_limiter():
    limiter = TokenBucketRateLimiter(requests_per_minute=10, tokens_per_minute=1000)
    acquired = await limiter.acquire(estimated_tokens=100)
    assert acquired is True

@pytest.mark.asyncio
async def test_request_queue():
    q = RequestQueue(max_size=5)
    success = await q.enqueue(1, {"test": True}, deadline=10000000000.0)
    assert success is True
    item = await q.dequeue(timeout=1.0)
    assert item is not None
    assert item["data"]["test"] is True
