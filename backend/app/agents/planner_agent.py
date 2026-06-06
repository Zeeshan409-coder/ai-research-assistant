from uuid import uuid4
from app.agents.base import BaseAgent
from app.schemas.research import ResearchPlan, ResearchTask


class PlannerAgent(BaseAgent):
    """
    Cognitive Planner Agent: Analyzes inbound complex human queries and 
    decomposes them into an ordered, deterministic sequence of actionable 
    sub-tasks assigned to specialized tracking workers.
    """

    @property
    def name(self) -> str:
        """Standardized abstract property implementation for tracking."""
        return "planner"

    async def run(self, query: str) -> ResearchPlan:
        """
        Asynchronously decomposes an input query string into a sequence of 
        ordered ResearchTasks wrapped inside a master operational ResearchPlan.
        """
        tasks = []

        # 🎯 Task Node 1: Multi-Tenant Internal Local RAG Extraction
        tasks.append(
            ResearchTask(
                task_id=str(uuid4()),
                description=f"Retrieve and parse internal vector knowledge context blocks for: {query}",
                task_type="retrieval",
                assigned_to="retriever"
            )
        )

        # 🎯 Task Node 2: Live Global External Internet Web Extraction
        tasks.append(
            ResearchTask(
                task_id=str(uuid4()),
                description=f"Search, scrape, and aggregate external knowledge networks for: {query}",
                task_type="web_search",
                assigned_to="web_search"
            )
        )

        # 🎯 Task Node 3: Grounded Ingestion Synthesis and Final Report Compile
        tasks.append(
            ResearchTask(
                task_id=str(uuid4()),
                description=f"Synthesize, cross-examine, and summarize all compiled evidence vectors for: {query}",
                task_type="summarization",
                assigned_to="summarizer"
            )
        )

        # Return the finalized deterministic execution roadmap
        return ResearchPlan(tasks=tasks)
