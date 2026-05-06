"""Analyst agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient


class AnalystAgent(BaseAgent):
    """Turns research notes into structured insights."""

    name = "analyst"

    def run(self, state: ResearchState) -> ResearchState:
        llm_client = LLMClient()
        
        system_prompt = (
            "You are a critical analyst. "
            "Analyze the research notes and extract key claims, viewpoints, and evidence. "
            "Point out any contradictions or weak evidence."
        )
        user_prompt = f"Analyze these research notes:\n{state.research_notes}"
        
        response = llm_client.complete(system_prompt, user_prompt)
        state.analysis_notes = response.content
        
        return state
