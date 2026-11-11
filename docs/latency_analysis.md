# Latency Analysis

## 1. Measured Slow Request Breakdown

For a heavy multi-hop query under burst load:

- **Admission & Queue Waiting**: 25ms (15%)
- **Retrieval (BM25)**: 12ms (7%)
- **Model Execution (TTFT)**: 95ms (56%)
- **Streaming Generation**: 30ms (18%)
- **Verification**: 8ms (4%)
- **Total Request Latency**: ~170ms

Observed measurements confirm that model execution (Time to First Token) dominates request latency.
