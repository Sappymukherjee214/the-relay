# Limit | Value found | How found | Confidence

|---|---|---|---|
| Requests per minute | 1,000 | Groq response header (`x-ratelimit-limit-requests`) | High |
| Tokens per minute | 8,000 | Groq response header (`x-ratelimit-limit-tokens`) | High |
| Requests per day | 14,400 | Estimated from RPM / free tier quotas | Medium |
| Tokens per day | 500,000 | Estimated quota | Medium |
| Requests in flight at once | 5 | Observed concurrency tests | High |
| What it returns when a limit is hit | HTTP 429 Too Many Requests | Live API response | High |
| Time until it recovers | 60 seconds rolling window | Rate-limit header reset | High |
