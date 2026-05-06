"""LangGraph workflow skeleton."""

from langgraph.graph import StateGraph, END
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.agents.supervisor import SupervisorAgent
from multi_agent_research_lab.agents.researcher import ResearcherAgent
from multi_agent_research_lab.agents.analyst import AnalystAgent
from multi_agent_research_lab.agents.writer import WriterAgent


class MultiAgentWorkflow:
    """Builds and runs the multi-agent graph.

    Keep orchestration here; keep agent internals in `agents/`.
    """

    def __init__(self):
        self.supervisor = SupervisorAgent()
        self.researcher = ResearcherAgent()
        self.analyst = AnalystAgent()
        self.writer = WriterAgent()

    def build(self) -> object:
        """Create and compile a LangGraph graph."""
        graph = StateGraph(ResearchState)

        # 1. Thêm các Nodes (Mỗi Agent là 1 node)
        graph.add_node("supervisor", self.supervisor.run)
        graph.add_node("researcher", self.researcher.run)
        graph.add_node("analyst", self.analyst.run)
        graph.add_node("writer", self.writer.run)

        # 2. Set điểm xuất phát là Supervisor
        graph.set_entry_point("supervisor")

        # 3. Hàm router đọc lịch sử route để rẽ nhánh
        def router(state: ResearchState) -> str:
            if not state.route_history:
                return END
            last_route = state.route_history[-1]
            return END if last_route == "done" else last_route

        # 4. Thêm Conditional Edges từ Supervisor đi các phòng ban
        graph.add_conditional_edges(
            "supervisor",
            router,
            {
                "researcher": "researcher",
                "analyst": "analyst",
                "writer": "writer",
                END: END
            }
        )

        # 5. Các nhân viên làm xong đều phải nộp lại cho Supervisor kiểm duyệt
        graph.add_edge("researcher", "supervisor")
        graph.add_edge("analyst", "supervisor")
        graph.add_edge("writer", "supervisor")

        return graph.compile()

    def run(self, state: ResearchState) -> ResearchState:
        """Execute the graph and return final state."""
        app = self.build()
        result = app.invoke(state)
        
        # result trả về có thể là dictionary, ta cần parse lại thành Pydantic object
        if isinstance(result, dict):
            return ResearchState(**result)
        return result
