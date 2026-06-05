from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.postgres import Base


class RAGEvaluation(Base):
    __tablename__ = "rag_evaluations"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    workspace_id = Column(String, ForeignKey("workspaces.id", ondelete="CASCADE"), index=True, nullable=False)
    conversation_id = Column(String, ForeignKey("conversations.id", ondelete="CASCADE"), index=True, nullable=False)

    # ⏱️ Latency & System Utilization Metrics
    total_latency_ms = Column(Integer, nullable=False)
    retrieval_latency_ms = Column(Integer, nullable=False)
    rerank_latency_ms = Column(Integer, nullable=False)
    llm_latency_ms = Column(Integer, nullable=False)
    tokens_used = Column(Integer, default=0, nullable=False)

    # 📊 Context Retrieval Metrics
    retrieval_hit_rate = Column(Float, nullable=False)       # Percentage of relevant chunks captured
    citation_coverage = Column(Float, nullable=False)        # Ratio of cited text vs full LLM output text
    reranker_effectiveness = Column(Float, nullable=False)   # Score delta before vs after cross-encoder processing

    # 🔬 LLM Answer Quality Real-Time Evaluations
    hallucination_detected = Column(Boolean, default=False, nullable=False)
    faithfulness_score = Column(Float, nullable=False)       # Is the answer derived *exclusively* from context?
    answer_relevance_score = Column(Float, nullable=False)   # Does the answer actually match the user query intent?

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    # Relational tracking connectors
    user = relationship("User")
    workspace = relationship("Workspace")
