from app.agents.base import BaseAgent
from app.services.llm_service import generate_response


class SummarizerAgent(BaseAgent):
    """
    Summarizer Agent: The final cognitive worker in the pipeline, tasked with 
    cross-examining all gathered evidence, filtering out hallucinations, and 
    synthesizing an objective, multi-sectional enterprise research report.
    """

    @property
    def name(self) -> str:
        """Standardized abstract property implementation for tracking."""
        return "summarizer"

    async def run(self, query: str, evidence: str) -> str:
        """
        Asynchronously formats gathered research material strings into a structured 
        contextual prompt and fires your local llama3.2 inference weights.
        """
        prompt = f"""You are an elite, enterprise-grade research analyst assistant. 
Your objective is to compile an objective, factual, and fully grounded final report based EXCLUSIVELY on the provided evidence material vectors.

Core Directives:
- Remain strictly faithful to the provided evidence strings.
- Cite your sources clearly within each section where facts are declared.
- If data points conflict, neutrally present both angles without fabricating values.

User Investigation Intent:
{query}

Compiled Evidence Dossier:
{evidence}

Generate a comprehensive structured research report following this layout template:

# EXECUTIVE RESEARCH ANALYSIS REPORT
## 🔍 KEY FINDINGS & CRITICAL METRICS
[Provide high-density bullet points of major verified takeaways]

## 📋 EVIDENCE COMPILATION SUMMARY
[Synthesize and cross-reference details pulled from internal vs external nodes]

## 🛡️ FINAL SYNTHESIS & RECOGNITION ANSWER
[Deliver your definitive concluding analysis fully cited back to sources]
"""

        # Dispatch the contextual block to your local model weights
        report_output = generate_response(prompt)
        return report_output
