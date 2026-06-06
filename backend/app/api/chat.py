import time
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.user import User
from app.models.workspace import Workspace
from app.dependencies.auth import get_current_user
from app.services.hybrid_service import hybrid_search
from app.services.prompt_service import build_prompt
from app.services.llm_service import generate_response
from app.services.retrieval_metrics import calculate_context_stats

# 📈 Phase 8.2 Core Telemetry Imports
from app.services.latency_tracker import LatencyTracker
from app.services.evaluation_service import EvaluationService, RetrievalMetrics, CitationMetrics

router = APIRouter()


class ChatRequest(BaseModel):
    workspace_id: str     
    conversation_id: str  
    query: str


@router.post("/chat")
async def chat(
    request: ChatRequest, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Start the master pipeline tracking stopwatch
    total_pipeline_timer = LatencyTracker()

    # 🛡️ Retrieval Security Layer: Verify ownership stakes
    workspace = db.query(Workspace).filter(Workspace.id == request.workspace_id).first()
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="The targeted research workspace could not be found."
        )
        
    if workspace.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You do not possess retrieval permissions for this workspace folder context."
        )

    # ⏱️ INSTRUMENTATION POINT A: Track Hybrid Vector + Sparse Retrieval Latency
    retrieval_timer = LatencyTracker()
    search_results = hybrid_search(
        query=request.query,
        workspace_id=request.workspace_id,
        top_k=5
    )
    retrieval_latency_ms = retrieval_timer.elapsed_ms()

    # Run the Prompt Engineering Compression Matrix Builder
    prompt, used_results = build_prompt(
        query=request.query,
        search_results=search_results,
        history=[],
        max_chars=8000
    )

    # Process baseline chunk performance counts and neural cross-encoder ranks
    retrieval_stats = RetrievalMetrics.calculate_metrics(used_results)
    context_stats = calculate_context_stats(used_results)

    # ⏱️ INSTRUMENTATION POINT B: Track Local LLM Inference Latency
    llm_timer = LatencyTracker()
    answer = generate_response(prompt)
    llm_latency_ms = llm_timer.elapsed_ms()

    # Calculate overall end-to-end request turnaround metrics
    total_latency_ms = total_pipeline_timer.elapsed_ms()

    # Extract clean citation metrics tracking objects
    citations = []
    for result in used_results:
        if isinstance(result, dict) and "metadata" in result:
            citations.append({
                "source": result["metadata"].get("source", "Unknown"),
                "page_number": result["metadata"].get("page_number", 0),
                "chunk_index": result["metadata"].get("chunk_index", 0),
                "rerank_score": result.get("rerank_score", result.get("score", 0.0))
            })

    # Calculate citation coverage ratio density
    coverage_score = CitationMetrics.citation_coverage(
        citations=citations, 
        retrieved_chunks=retrieval_stats["chunk_count"]
    )

    # 💾 OBSERVABILITY PERSISTENCE GATEWAY: Commit metrics into PostgreSQL
    EvaluationService.create_evaluation(
        db=db,
        user_id=current_user.id,
        workspace_id=request.workspace_id,
        conversation_id=request.conversation_id,
        query=request.query,
        answer=answer,
        retrieval_latency_ms=retrieval_latency_ms,
        llm_latency_ms=llm_latency_ms,
        total_latency_ms=total_latency_ms,
        retrieved_chunks=retrieval_stats["chunk_count"],
        citations_used=len(citations),
        reranked_chunks=retrieval_stats["chunk_count"],
        model_name="llama3.2",
        avg_rerank_score=retrieval_stats["avg_rerank_score"],
        citation_coverage=coverage_score,
        retrieval_score=retrieval_stats["avg_rerank_score"]
    )

    return {
        "workspace_id": request.workspace_id,
        "conversation_id": request.conversation_id,
        "query": request.query,
        "answer": answer,
        "metrics": {
            **context_stats,
            "total_latency_ms": total_latency_ms,
            "retrieval_latency_ms": retrieval_latency_ms,
            "llm_latency_ms": llm_latency_ms,
            "citation_coverage": coverage_score,
            "avg_rerank_score": retrieval_stats["avg_rerank_score"]
        },
        "citations": citations
    }
