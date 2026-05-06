"""Search client abstraction for ResearcherAgent."""

import requests
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.schemas import SourceDocument
from multi_agent_research_lab.core.config import get_settings


class SearchClient:
    """Provider-agnostic search client skeleton."""

    def __init__(self):
        self.api_key = get_settings().tavily_api_key

    def search(self, query: str, max_results: int = 5) -> list[SourceDocument]:
        """Search for documents relevant to a query using Tavily API."""
        if not self.api_key:
            # Fallback mock if Tavily key is missing
            return [
                SourceDocument(
                    title="Mock Document", 
                    url="https://mock.example.com", 
                    snippet="This is a mock search result because TAVILY_API_KEY is not set."
                )
            ]

        try:
            response = requests.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": self.api_key,
                    "query": query,
                    "max_results": max_results,
                    "search_depth": "basic",
                    "include_answer": False
                },
                timeout=15
            )
            response.raise_for_status()
            data = response.json()
            
            documents = []
            for item in data.get("results", []):
                documents.append(SourceDocument(
                    title=item.get("title", "Untitled"),
                    url=item.get("url", ""),
                    snippet=item.get("content", "")
                ))
            return documents
            
        except Exception as e:
            raise RuntimeError(f"Tavily search failed: {e}")
