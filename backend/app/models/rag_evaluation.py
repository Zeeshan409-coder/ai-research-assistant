from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from app.db.postgres import Base


class RAGEvaluation(Base):
    __tablename__ = "rag_evaluations"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    workspace_id = Column(String, ForeignKey("workspaces.id", ondelete="CASCADE"), index=True, nullable=False)
    conversation_id = Column(String, ForeignKey("conversations.id", ondelete="CASCADE"), index=True, nullable=False)

    # 📝 Raw Text Audit Fields (Step 6 Naming Expansion)
    query = Column(Text, nullable=True)   
    answer = Column(Text, nullable=True)  

    # ⏱️ Latency & System Utilization Metrics
    total_latency_ms = Column(Integer, nullable=False)
    retrieval_latency_ms = Column(Integer, nullable=False)
    rerank_latency_ms = Column(Integer, nullable=False)
    llm_latency_ms = Column(Integer, nullable=False)
    tokens_used = Column(Integer, default=0, nullable=False)

    # 📊 Core Quality Analytics Tracking Columns
    avg_rerank_score = Column(Float, default=0.0, nullable=False)
    citation_coverage = Column(Float, default=0.0, nullable=False)
    retrieval_score = Column(Float, default=0.0, nullable=False)
    
    retrieved_chunks = Column(Integer, default=0, nullable=False)
    citations_used = Column(Integer, default=0, nullable=False)
    reranked_chunks = Column(Integer, default=0, nullable=False)
    model_name = Column(String, default="llama3.2", nullable=False)

    # 🔬 LLM Answer Quality Real-Time Evaluations
    hallucination_detected = Column(Boolean, default=False, nullable=False)
    faithfulness_score = Column(Float, default=1.0, nullable=False)
    answer_relevance_score = Column(Float, default=1.0, nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    # Relational tracking connectors
    user = relationship("User")
    workspace = relationship("Workspace")
