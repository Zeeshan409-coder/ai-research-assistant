from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import List, Dict, Any

from app.db.dependencies import get_db
from app.models.user import User
from app.models.rag_evaluation import RAGEvaluation
from app.dependencies.auth import get_current_user
from app.services.evaluation_service import EvaluationAnalytics

router = APIRouter(
    prefix="/analytics",
    tags=["RAG Analytics & Observability"]
)


@router.get("/evaluations")
def get_latest_evaluations(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Observability Stream: Streams back the latest chronologically recorded RAG pipeline 
    evaluation, performance tracing, and metric records for the authenticated user.
    """
    records = db.query(RAGEvaluation)\
        .filter(RAGEvaluation.user_id == current_user.id)\
        .order_by(RAGEvaluation.created_at.desc())\
        .limit(limit)\
        .all()
        
    return records


@router.get("/evaluations/stats")
def get_aggregated_rag_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Telemetry Dashboard Aggregator: Computes mathematical runtime analytics averages 
    across latency distribution tiers and retrieval quality indexes to power frontend charts.
    """
    # 1. Execute optimized aggregate scalar queries filtered strictly by active owner boundaries
    stats_query = db.query(
        func.avg(RAGEvaluation.total_latency_ms).label("avg_total"),
        func.avg(RAGEvaluation.retrieval_latency_ms).label("avg_retrieval"),
        func.avg(RAGEvaluation.llm_latency_ms).label("avg_llm"),
        func.count(RAGEvaluation.id).label("total_reqs"),
    ).filter(RAGEvaluation.user_id == current_user.id).first()

    # 2. Extract calculations fallback values gracefully if no evaluation rows exist yet
    avg_latency = float(stats_query.avg_total) if stats_query.avg_total is not None else 0.0
    avg_retrieval = float(stats_query.avg_retrieval) if stats_query.avg_retrieval is not None else 0.0
    avg_llm = float(stats_query.avg_llm) if stats_query.avg_llm is not None else 0.0
    total_requests = int(stats_query.total_reqs) if stats_query.total_reqs is not None else 0

    # 3. Extract advanced RAG context retrieval matrix parameters natively via our service helper
    retrieval_quality = EvaluationAnalytics.get_retrieval_quality_metrics(db, user_id=current_user.id)

    return {
        "avg_latency_ms": round(avg_latency, 2),
        "avg_retrieval_ms": round(avg_retrieval, 2),
        "avg_llm_ms": round(avg_llm, 2),
        "total_requests": total_requests,
        "retrieval_quality": retrieval_quality
    }
