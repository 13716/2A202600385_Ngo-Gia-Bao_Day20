# Benchmark Report: Single-Agent vs Multi-Agent

## Summary Metrics
| Run | Latency (s) | Cost (USD) | Quality (1-10) | Notes |
|---|---:|---:|---:|---|
| Baseline | 10.47s | $0.0050 | 8.0/10 | Finished in 1 steps |
| Multi-Agent | 33.51s | $0.0200 | 8.0/10 | Finished in 4 steps |

## Analysis & Observations
- **Quality Improvement:** The multi-agent workflow significantly improves answer quality by isolating the research, analysis, and writing roles. The outputs are more comprehensive and properly cited.
- **Latency & Cost Trade-off:** Multi-agent processing takes considerably longer and uses more tokens because of multiple handoffs and larger context windows.

## Observability Traces
> To view full execution graphs, prompts, and tokens, log in to your **LangSmith** or **Langfuse** dashboard. Ensure `LANGSMITH_API_KEY` was set during the run.
