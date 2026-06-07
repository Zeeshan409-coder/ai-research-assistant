from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from app.db.postgres import Base


class AgentExecution(Base):
    __tablename__ = "agent_executions"

    id = Column(String, primary_key=True)
    workspace_id = Column(String, ForeignKey("workspaces.id", ondelete="CASCADE"), index=True, nullable=False)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    
    # ⏱️ Core Telemetry Tracing Metrics
    agent_name = Column(String, index=True, nullable=False)   # e.g., 'planner', 'retriever', 'web_search', 'summarizer'
    query = Column(Text, nullable=True)
    latency_ms = Column(Integer, nullable=False)
    success = Column(Boolean, default=True, nullable=False)
    
    start_time = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    end_time = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relational connection components
    workspace = relationship("Workspace")
    user = relationship("User")
