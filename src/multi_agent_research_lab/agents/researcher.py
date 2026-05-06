"""Researcher agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.search_client import SearchClient
from multi_agent_research_lab.services.llm_client import LLMClient


class ResearcherAgent(BaseAgent):
    """Collects sources and creates concise research notes."""

    name = "researcher"

    def run(self, state: ResearchState) -> ResearchState:
        # 1. Initialize tools
        search_client = SearchClient()
        llm_client = LLMClient()
        
        # 2. Search for information
        query = state.request.query
        max_sources = state.request.max_sources
        sources = search_client.search(query, max_results=max_sources)
        state.sources = sources
        
        # 3. Compile sources into a single string for LLM
        sources_text = "\n\n".join([
            f"Title: {s.title}\nURL: {s.url}\nContent: {s.snippet}"
            for s in sources
        ])
        
        # 4. Synthesize research notes
        system_prompt = (
            "You are a meticulous researcher. "
            "Extract the most important facts, figures, and claims from the provided search results. "
            "Summarize them clearly as research notes. Do not hallucinate. Include citations if possible."
        )
        user_prompt = f"Target Query: {query}\n\nSearch Results:\n{sources_text}"
        
        response = llm_client.complete(system_prompt, user_prompt)
        state.research_notes = response.content
        
        return state
