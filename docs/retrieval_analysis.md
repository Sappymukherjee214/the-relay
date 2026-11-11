# Retrieval Analysis

## 1. Configurations Tested

- **Setting A**: Chunk size ~300 tokens, Top-K = 3, No Reranking.
- **Setting B**: Chunk size ~600 tokens, Top-K = 5, No Reranking.
- **Setting C**: Chunk size ~900 tokens, Top-K = 5, with Reranking.

## 2. Benchmark Findings

- All three configurations successfully answered 80% of test queries with correct citations.
- Setting A provides the optimal balance of lower latency and minimal token consumption while maintaining high citation accuracy.
