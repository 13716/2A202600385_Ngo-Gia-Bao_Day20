"""Supervisor / router skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.core.config import get_settings
from multi_agent_research_lab.core.schemas import AgentName


class SupervisorAgent(BaseAgent):
    """Decides which worker should run next and when to stop."""

    name = "supervisor"

    def run(self, state: ResearchState) -> ResearchState:
        settings = get_settings()

        # 1. Enforce max iterations fallback
        if state.iteration >= settings.max_iterations:
            if not state.final_answer:
                state.record_route(AgentName.WRITER)
                return state
            state.record_route("done")
            return state

        # 2. Inspect missing fields to determine next step
        if not state.research_notes and not state.sources:
            next_agent = AgentName.RESEARCHER
        elif not state.analysis_notes:
            next_agent = AgentName.ANALYST
        elif not state.final_answer:
            next_agent = AgentName.WRITER
        else:
            next_agent = "done"

        # 3. Update state with the chosen route
        state.record_route(next_agent)
        return state
