from fastapi import APIRouter
from app.services.hybrid_service import hybrid_search
from app.services.retrieval_metrics import calculate_context_stats  # 👈 Added metrics

router = APIRouter()


@router.get("/search")
async def semantic_search(query: str):

    results = hybrid_search(query)
    context_stats = calculate_context_stats(results)

    formatted = []
    for result in results:
        formatted.append({
            "rerank_score": result["rerank_score"],
            "rrf_score": result["rrf_score"],
            "source": result["metadata"]["source"],
            "page_number": result["metadata"]["page_number"],
            "text": result["text"]
        })

    return {
        "metrics": context_stats,  # 👈 Returning character/chunk analytics
        "results": formatted
    }
