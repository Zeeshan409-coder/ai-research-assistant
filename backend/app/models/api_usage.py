from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.postgres import Base


class APIUsage(Base):
    __tablename__ = "api_usage"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    
    # Core Metered Analytics Metrics Tracks
    requests_count = Column(Integer, default=0, nullable=False)
    tokens_consumed = Column(Integer, default=0, nullable=False)
    retrieval_calls = Column(Integer, default=0, nullable=False)
    
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relational tracking connectors
    user = relationship("User")
