from app.agents.base import BaseAgent
from app.services.search_provider import TavilySearchProvider
from app.schemas.research import ResearchEvidence
from typing import List


class WebSearchAgent(BaseAgent):
    """
    Web Search Agent: An interchangeable tool worker tasked with harvesting, 
    parsing, and formatting live external internet knowledge context snippets
    leveraging abstracted search providers.
    """

    def __init__(self):
        """Initializes the agent with an encapsulated search infrastructure abstraction."""
        self.provider = TavilySearchProvider()

    @property
    def name(self) -> str:
        """Standardized abstract property implementation for tracking."""
        return "web_search"

    async def run(self, query: str) -> List[ResearchEvidence]:
        """
        Asynchronously triggers external web queries through the provider 
        and bundles the returned assets cleanly into standardized ResearchEvidence schema items.
        """
        search_results = await self.provider.search(
            query=query,
            max_results=5
        )

        evidence = []

        # 🛡️ Structural Fallback Guard: Support both raw nested dictionary payloads 
        # and clean pre-mapped provider list arrays effortlessly.
        raw_list = []
        if isinstance(search_results, dict):
            raw_list = search_results.get("results", [])
        elif isinstance(search_results, list):
            raw_list = search_results

        # Iterate and map text records into structural agent data contracts
        for result in raw_list:
            if isinstance(result, dict):
                evidence.append(
                    ResearchEvidence(
                        source=result.get("url", result.get("title", "External Web Link")),
                        content=result.get("content", "Empty external web segment context."),
                        evidence_type="web",
                        score=0.85 # Stable external web confidence score weight marker
                    )
                )

        return evidence
