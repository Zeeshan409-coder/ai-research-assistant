from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.postgres import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="SET NULL"), index=True, nullable=True) # Retain logs even if user accounts are soft-purged later
    
    # Core Audit Fields
    action = Column(String, nullable=False)        # e.g., 'DOCUMENT_UPLOAD', 'WORKSPACE_DELETION', 'CONTEXT_SEARCH'
    resource_type = Column(String, nullable=False) # e.g., 'workspace', 'document', 'chat'
    resource_id = Column(String, nullable=True)   # The specific database tracking ID string target
    details = Column(Text, nullable=True)         # JSON string or plain text notes capturing additional payload context metadata
    
    ip_address = Column(String, nullable=True)    # Captures networking origins for advanced threat monitoring
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    # Relational connection layer
    user = relationship("User")
