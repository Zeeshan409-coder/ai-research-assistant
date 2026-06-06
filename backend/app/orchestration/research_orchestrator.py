from app.agents.planner_agent import PlannerAgent
from app.agents.retriever_agent import RetrieverAgent
from app.agents.summarizer_agent import SummarizerAgent


class ResearchOrchestrator:
    def __init__(self):
        """
        Initializes a top-down, deterministic AI Research Orchestrator core framework
        loaded with modular cognitive planners, search engines, and synthesis systems.
        """
        self.planner = PlannerAgent()
        self.retriever = RetrieverAgent()
        self.summarizer = SummarizerAgent()

    async def execute(self, workspace_id: str, query: str) -> dict:
        """
        Asynchronously manages the top-down lifecycle of an advanced agentic research 
        investigation task from initial planning to final multi-sectional report compilation.
        """
        # 🛡️ Step 1: Initialize the top-down deterministic tasks roadmap
        plan = await self.planner.run(query)

        # 🛡️ Step 2: Route execution parameters down to the Retriever Agent
        retrieval_results = await self.retriever.run(
            workspace_id=workspace_id,
            query=query
        )

        # 🛡️ Step 3: Unpack Pydantic ResearchEvidence models into an analytical dossier string
        evidence_blocks = []
        for r in retrieval_results:
            evidence_blocks.append(
                f"[Source: {r.source} (Relevance Rank: {r.score})]\n"
                f"Content Excerpt:\n{r.content}"
            )
            
        evidence_dossier = "\n\n---\n\n".join(evidence_blocks)

        # 🛡️ Step 4: Dispatch the collected dossier to the Summarizer Agent for report compile
        report = await self.summarizer.run(
            query=query,
            evidence=evidence_dossier
        )

        # 🛡️ Step 5: Consolidate comprehensive tracking details to return back to routers
        return {
            "plan": plan.dict(), # Serializes the Pydantic plan object cleanly
            "report": report,
            "retrieved_chunks_count": len(retrieval_results),
            "evidence_summary": [r.dict() for r in retrieval_results]
        }
