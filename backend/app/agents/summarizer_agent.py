from typing import Any
from app.agents.base import BaseAgent
from app.services.llm_service import generate_response


class SummarizerAgent(BaseAgent):
    """
    Cognitive Summarizer Agent (Phase 9.3 Definitive): Evaluates fused knowledge dossiers 
    alongside multi-agent audit critiques and fact-verification logs to synthesize 
    an enterprise-grade research report that is completely self-reviewed before generation.
    """

    @property
    def name(self) -> str:
        """Standardized abstract property implementation for tracking."""
        return "summarizer"

    async def run(self, query: str, evidence: list, critique: Any, verification: Any) -> str:
        """
        Asynchronously formats fused knowledge text blocks, quality critique points, 
        and factional reliability logs into a comprehensive cross-examined LLM prompt.
        """
        context = ""

        # 1. Structure the multi-silo knowledge context strings
        for item in evidence:
            source_info = f" (Source: {item.get('source', 'Unknown')})"
            if item.get("type") == "internal":
                context += f"[INTERNAL DATA SILO]{source_info}\n{item.get('content', '')}\n\n"
            else:
                context += f"[LIVE WEB INTEL SILO]{source_info}\n{item.get('content', '')}\n\n"

        # 2. Inject raw analytical payloads straight into the synthesis pass matrix prompt
        prompt = f"""You are an elite, enterprise-grade AI research analyst supervisor.
Your mission is to compile a highly structured, objective, and deeply comprehensive Research Report by cross-examining internal repository records with fresh live internet intelligence, actively accounting for the provided quality audit logs.

Operational Directives:
- Prioritize internal corporate vector findings.
- Use live web data to supplement, metricize, or fill data gaps.
- Factor in the self-review critiques and factual verifications below to build an auditable, halluncination-free report.

Target User Investigation Intent:
{query}

Fused Multi-Silo Evidence Dossier:
{context}

---
🤖 MULTI-AGENT SELF-REVIEW CRITIQUE ANALYSIS:
{critique}

---
🛡️ MULTI-AGENT FACT-VERIFICATION ANALYSIS:
{verification}
---

Generate the final enterprise report precisely matching this multi-sectional structural template:

# 📋 ENTERPRISE RESEARCH SPECIFICATION & SYNTHESIS REPORT

## ⚡ 1. EXECUTIVE SUMMARY
[Deliver a high-level summary overview answering the query intent concisely]

## 🏢 2. INTERNAL COMPLIANCE & REPOSITORY FINDINGS
[Synthesize critical insights extracted exclusively from internal workspace files]

## 🌐 3. EXTERNAL INTELLIGENCE & MARKET TRENDS
[Integrate supplementary metrics and real-time parameters captured from web channels]

## ⚠️ 4. ANOMALIES, RISKS & DATA CONTRADICTIONS
[Explicitly call out the information gaps, unsupported claims, and contradictions flagged by our multi-agent self-review logs above. Address their potential impact on data integrity.]

## 🛡️ 5. DEFINITIVE ANALYTICAL CONCLUSION
[Provide your concluding analytical resolution, fully grounded and backed back to source markers]
"""

        # Dispatch the self-corrected context prompt down to your local LLM inference worker
        return generate_response(prompt)
