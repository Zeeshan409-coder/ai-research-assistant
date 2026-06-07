from app.agents.base import BaseAgent
from app.services.llm_service import generate_response


class SummarizerAgent(BaseAgent):
    """
    Cognitive Summarizer Agent (Phase 9.2): Evaluates fused multi-silo knowledge 
    dossiers to isolate internal corporate vector findings from live external web insights, 
    cross-references data integrity, and compiles an advanced enterprise research report.
    """

    @property
    def name(self) -> str:
        """Standardized abstract property implementation for tracking."""
        return "summarizer"

    async def run(self, query: str, evidence: list) -> str:
        """
        Asynchronously builds a multi-domain context frame from fused evidence dictionaries 
        and dispatches a comprehensive analytical instructions prompt to local llama3.2 weights.
        """
        context = ""

        # Construct structured domain separation context markers for the prompt matrix
        for item in evidence:
            source_info = f" (Source: {item.get('source', 'Unknown')})"
            if item.get("type") == "internal":
                context += f"[INTERNAL DATA SILO]{source_info}\n{item['content']}\n\n"
            else:
                context += f"[LIVE WEB INTEL SILO]{source_info}\n{item['content']}\n\n"

        prompt = f"""You are an elite, enterprise-grade AI research analyst supervisor.
Your mission is to compile a highly structured, objective, and deeply comprehensive Research Report by cross-examining internal repository records with fresh live internet intelligence.

Strict Ingestion Protocols:
1. PRIORITIZE INTERNAL REPOSITORY DATA: Treat local workspace records as your primary truth matrix.
2. SUPPLEMENT WITH LIVE WEB INTEL: Use external web evidence exclusively to add modern context, bridge knowledge gaps, or add timely metrics.
3. CONFLICT IDENTIFICATION: Actively check for contradictions between internal records and web text (e.g., conflicting dates, versions, stats). Flag these explicitly.
4. ABSOLUTE ZERO HALLUCINATION: Declare claims as facts ONLY if they are directly derived from the provided evidence data string nodes below.

Target Investigation Request:
{query}

Fused Multi-Silo Evidence Dossier:
{context}

Generate the final enterprise report precisely matching this multi-sectional structural template:

# 📋 ENTERPRISE RESEARCH SPECIFICATION & SYNTHESIS REPORT

## ⚡ 1. EXECUTIVE SUMMARY
[Deliver a high-level summary overview answering the query intent concisely]

## 🏢 2. INTERNAL COMPLIANCE & REPOSITORY FINDINGS
[Synthesize critical insights extracted exclusively from internal workspace files]

## 🌐 3. EXTERNAL INTELLIGENCE & MARKET TRENDS
[Integrate supplementary metrics and real-time parameters captured from web channels]

## ⚠️ 4. ANOMALIES, RISKS & DATA CONTRADICTIONS
[Explicitly map out any metric deviations, discrepancies, or conflicts found between internal files and external links. If none exist, explicitly state: 'No multi-silo data discrepancies identified.']

## 🛡️ 5. DEFINITIVE ANALYTICAL CONCLUSION
[Provide your concluding analytical resolution, fully grounded and backed back to source markers]
"""

        # Dispatch the fused context prompt down to your local LLM inference worker
        return generate_response(prompt)
