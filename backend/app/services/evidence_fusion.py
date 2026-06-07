from typing import List, Dict, Any
from app.schemas.research import ResearchEvidence

def fuse_evidence(internal_chunks: List[Any], web_results: List[ResearchEvidence]) -> List[Dict[str, Any]]:
    """
    Evidence Fusion Core: Combines multi-tenant private vector data slices 
    with live web-scraped/search intelligence into a standardized chronological dossier.
    """
    evidence = []

    # 1. Process internal document knowledge base chunks safely
    for chunk in internal_chunks:
        # Support both Pydantic objects and raw dictionary formats seamlessly
        if hasattr(chunk, "content"):
            content_str = chunk.content
            source_str = getattr(chunk, "source", "Internal Document")
        elif isinstance(chunk, dict):
            content_str = chunk.get("text", chunk.get("content", "Empty context"))
            source_str = chunk.get("metadata", {}).get("source", "Internal Document")
        else:
            content_str = str(chunk)
            source_str = "Internal Document"

        evidence.append({
            "type": "internal",
            "content": content_str,
            "source": source_str
        })

    # 2. Merge live global internet web results concurrently
    for web in web_results:
        evidence.append({
            "type": "web",
            "content": web.content,
            "source": web.source
        })

    return evidence
