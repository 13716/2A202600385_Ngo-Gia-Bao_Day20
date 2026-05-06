# 🔬 Multi-Agent Research Lab

This repository contains a fully functional Multi-Agent System built with **LangGraph**, **OpenAI**, and **Tavily**. The system simulates a professional research workflow by coordinating multiple specialized AI agents to gather, analyze, and synthesize information into a comprehensive report.

## 🏗️ Architecture & Project Structure

The project uses a **Hub-and-Spoke** architecture where a central `Supervisor` agent routes tasks to specialized worker agents based on the current state of the research.

```text
src/multi_agent_research_lab/
├── agents/
│   ├── base.py         # Abstract base class for all agents
│   ├── supervisor.py   # The central router/manager
│   ├── researcher.py   # Information gatherer (uses Tavily API)
│   ├── analyst.py      # Fact-checker and critical thinker
│   └── writer.py       # Final report synthesizer
├── core/
│   ├── config.py       # Pydantic settings & Env vars validation
│   ├── schemas.py      # Pydantic schemas for state/documents
│   └── state.py        # Shared ResearchState
├── evaluation/         # Benchmarking tools (LLM-as-a-judge & Cost estimation)
├── graph/              # LangGraph workflow orchestration
├── observability/      # Tracing hooks
└── services/           # External API Clients (OpenAI, Tavily)
```

## ⚙️ Setup Instructions

### 1. Create a Virtual Environment
It is highly recommended to use a virtual environment.
```bash
python -m venv .venv

# On Windows:
.\.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate
```

### 2. Install Dependencies
Install the package in editable mode along with developer and LLM dependencies:
```bash
pip install -e ".[dev,llm]"
```

### 3. Environment Variables
Copy the `.env.example` file to `.env` and fill in your API keys:
```bash
cp .env.example .env
```
Inside `.env`, you must provide the following keys:
- `OPENAI_API_KEY`: Your OpenAI key.
- `TAVILY_API_KEY`: Your Tavily Search API key.
- `LANGSMITH_API_KEY`: (Optional) For LangSmith tracing.
- `LANGCHAIN_TRACING_V2=true`: (Optional) Enable tracing.

---

## 🚀 How to Run the Program

### 1. Single-Agent Baseline
Run a standard, single LLM prompt. This serves as a baseline to compare against the multi-agent system:
```bash
python -m multi_agent_research_lab.cli baseline --query "What are the latest advancements in GraphRAG?"
```

### 2. Multi-Agent Workflow
Run the full Multi-Agent system. You will see the Supervisor intelligently route the query to the Researcher, Analyst, and Writer before returning the final JSON response:
```bash
python -m multi_agent_research_lab.cli multi-agent --query "What are the latest advancements in GraphRAG?"
```

---

## 📊 Benchmarking & Evaluation

To automatically compare the Single-Agent vs. Multi-Agent approach, run the benchmarking script. It runs both workflows, measures latency, estimates token costs, and uses an **LLM-as-a-judge** to score the final quality.

```bash
python run_bench.py
```
*Note: The results will be automatically formatted and saved as a markdown report in `reports/benchmark_report.md`.*

---

## 🧪 Testing
To run the automated test suite and verify all modules are working correctly:
```bash
pytest -v
```

---

## 👁️ Observability
This project is fully integrated with **LangSmith**. If you provided your `LANGSMITH_API_KEY` and set `LANGCHAIN_TRACING_V2=true` in your `.env` file, all Multi-Agent interactions, prompts, LLM parameters, and token usage are automatically traced and uploaded to your [LangSmith Dashboard](https://smith.langchain.com/).
