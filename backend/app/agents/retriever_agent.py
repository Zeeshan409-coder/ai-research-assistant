from app.agents.base import BaseAgent
from app.services.hybrid_service import hybrid_search
from app.schemas.research import ResearchEvidence
from typing import List


class RetrieverAgent(BaseAgent):
    """
    Retriever Agent: An encapsulated data harvesting worker tasked with extracting,
    ranking, and verifying relevant knowledge context chunks from private multi-tenant vector databases.
    """

    @property
    def name(self) -> str:
        """Standardized abstract property implementation for tracking."""
        return "retriever"

    async def run(self, workspace_id: str, query: str) -> List[ResearchEvidence]:
        """
        Asynchronously executes your highly optimized, dual-layer hybrid search pipeline 
        and maps the raw chunk payload array into a standardized set of ResearchEvidence schema outputs.
        """
        # Execute your existing production hybrid vector + dense database search
        # Parameter aligned: uses top_k matching blocks cleanly
        raw_results = hybrid_search(
            query=query,
            workspace_id=workspace_id,
            top_k=5
        )

        evidence_list = []
        
        # Transform unstructured database dictionaries into structural agent contracts
        for result in raw_results:
            if isinstance(result, dict) and "metadata" in result:
                metadata = result["metadata"]
                source_title = metadata.get("source", "Unknown Internal File")
                page_info = f" (Page {metadata.get('page_number', 1)})" if "page_number" in metadata else ""
                
                evidence_list.append(
                    ResearchEvidence(
                        source=f"{source_title}{page_info}",
                        content=result.get("text", result.get("content", "")),
                        evidence_type="local_rag",
                        score=float(result.get("rerank_score", result.get("score", 0.0)))
                    )
                )

        return evidence_list
