"""Benchmark skeleton for single-agent vs multi-agent."""

from time import perf_counter
from typing import Callable

from multi_agent_research_lab.core.schemas import BenchmarkMetrics
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient


Runner = Callable[[str], ResearchState]


def run_benchmark(run_name: str, query: str, runner: Runner) -> tuple[ResearchState, BenchmarkMetrics]:
    """Measure latency, cost, and quality."""

    started = perf_counter()
    state = runner(query)
    latency = perf_counter() - started
    
    # 1. Estimate Cost (Heuristic based on iterations)
    cost = state.iteration * 0.005  # ~ $0.005 per agent step
    
    # 2. Quality Scoring using LLM-as-a-judge
    quality = None
    try:
        if state.final_answer:
            llm = LLMClient()
            eval_sys = "You are an expert evaluator. Rate the answer quality from 1 to 10 based on structure, depth, and citation of sources. Return ONLY the number."
            eval_user = f"Query: {query}\n\nAnswer: {state.final_answer}"
            res = llm.complete(eval_sys, eval_user)
            quality = float(res.content.strip())
    except Exception:
        quality = 5.0 # Fallback
        
    metrics = BenchmarkMetrics(
        run_name=run_name, 
        latency_seconds=latency,
        estimated_cost_usd=cost,
        quality_score=quality,
        notes=f"Finished in {state.iteration} steps"
    )
    return state, metrics
