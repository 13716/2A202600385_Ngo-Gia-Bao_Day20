"""Writer agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient


class WriterAgent(BaseAgent):
    """Produces final answer from research and analysis notes."""

    name = "writer"

    def run(self, state: ResearchState) -> ResearchState:
        llm_client = LLMClient()
        
        system_prompt = (
            "You are a clear and concise technical writer. "
            "Synthesize the research notes and critical analysis into a final report. "
            "If the analysis points out contradictions, briefly mention them with nuance. "
            "Keep the tone neutral and professional."
        )
        user_prompt = f"Target Query: {state.request.query}\n\nResearch Notes:\n{state.research_notes}\n\nAnalysis:\n{state.analysis_notes}"
        
        response = llm_client.complete(system_prompt, user_prompt)
        state.final_answer = response.content
        
        return state
