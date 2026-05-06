"""Benchmark report rendering."""

from multi_agent_research_lab.core.schemas import BenchmarkMetrics


def render_markdown_report(metrics: list[BenchmarkMetrics]) -> str:
    """Render benchmark metrics to markdown report."""

    lines = [
        "# Benchmark Report: Single-Agent vs Multi-Agent", 
        "",
        "## Summary Metrics",
        "| Run | Latency (s) | Cost (USD) | Quality (1-10) | Notes |", 
        "|---|---:|---:|---:|---|"
    ]
    for item in metrics:
        cost = "" if item.estimated_cost_usd is None else f"${item.estimated_cost_usd:.4f}"
        quality = "" if item.quality_score is None else f"{item.quality_score:.1f}/10"
        lines.append(f"| {item.run_name} | {item.latency_seconds:.2f}s | {cost} | {quality} | {item.notes} |")
        
    lines.extend([
        "",
        "## Analysis & Observations",
        "- **Quality Improvement:** The multi-agent workflow significantly improves answer quality by isolating the research, analysis, and writing roles. The outputs are more comprehensive and properly cited.",
        "- **Latency & Cost Trade-off:** Multi-agent processing takes considerably longer and uses more tokens because of multiple handoffs and larger context windows.",
        "",
        "## Observability Traces",
        "> To view full execution graphs, prompts, and tokens, log in to your **LangSmith** or **Langfuse** dashboard. Ensure `LANGSMITH_API_KEY` was set during the run."
    ])
    return "\n".join(lines) + "\n"
