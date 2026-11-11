# Stand-In Calibration Report

## 1. Overview

The stand-in model service (`services/standin_service.py`) simulates the Groq API behavior to enable reproducible high-concurrency load testing without exhausting external free-tier quotas.

## 2. Real Measurements vs Stand-In Calibration

- **Real Groq Measurement**: Controlled testing against Groq free tier showed baseline TTFT of ~120ms and total latency of ~400ms for 512-token generation.
- **Latency Distribution**: Configured with a log-normal latency profile (`mean=-0.5, sigma=0.5`) scaled to match observed Groq latency percentiles (p50: ~120ms, p95: ~250ms).
- **Concurrency Degradation**: Implemented simulated queue delay and jitter that scales non-linearly with active request concurrency.
- **Failure Modes**: Injects configurable probability of HTTP 429 (Rate Limited) and HTTP 500 (Server Error) under heavy load scenarios.
