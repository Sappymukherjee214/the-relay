# The Relay

A production-grade, rate-limit-aware research assistant processing engineering questions through a multi-stage LLM pipeline.

## Features
- **5-Stage Pipeline**: Request understanding, BM25 retrieval, decision/tool execution, answer generation, and citation verification.
- **Robust Rate Limiting**: Token-bucket rate limiter and bounded priority queue.
- **Stand-In Service**: FastAPI mock service simulating Groq latency, failure modes, and rate limits.
- **Load Experiments**: Automated scenarios (steady, burst, overload, halved limits, budget exhaustion) generating `results.csv`.
- **Retrieval Benchmark**: Evaluated configurations A, B, and C with comprehensive metrics.

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Download Papers & Extract**:
   ```bash
   python -m core.paper_downloader
   ```

3. **Run Stand-In Service**:
   ```bash
   uvicorn services.standin_service:app --port 8001
   ```

4. **Run Experiments & Benchmarks**:
   ```bash
   python -m experiments.run_experiment
   python -m experiments.retrieval_benchmark
   python -m experiments.analyze_results
   ```

5. **Run Tests**:
   ```bash
   pytest
   ```
