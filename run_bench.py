import os
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.graph.workflow import MultiAgentWorkflow
from multi_agent_research_lab.evaluation.benchmark import run_benchmark
from multi_agent_research_lab.evaluation.report import render_markdown_report

query = "What are the latest advancements in GraphRAG?"

# Baseline Runner
def baseline_runner(q: str) -> ResearchState:
    state = ResearchState(request=ResearchQuery(query=q))
    llm = LLMClient()
    res = llm.complete("You are an expert. Answer the user.", q)
    state.final_answer = res.content
    state.iteration = 1
    return state

# Multi-Agent Runner
def multi_agent_runner(q: str) -> ResearchState:
    state = ResearchState(request=ResearchQuery(query=q))
    workflow = MultiAgentWorkflow()
    return workflow.run(state)

print("Running Baseline...")
state_base, metric_base = run_benchmark("Baseline", query, baseline_runner)

print("Running Multi-Agent...")
state_multi, metric_multi = run_benchmark("Multi-Agent", query, multi_agent_runner)

report_content = render_markdown_report([metric_base, metric_multi])

# Save to reports/benchmark_report.md
os.makedirs("reports", exist_ok=True)
with open("reports/benchmark_report.md", "w", encoding="utf-8") as f:
    f.write(report_content)

print("Benchmark report saved to reports/benchmark_report.md")
