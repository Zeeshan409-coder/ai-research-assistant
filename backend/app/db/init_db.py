from app.db.postgres import engine, Base
# Explicitly import all multi-tenant relational models to register them inside the Base metadata catalog
from app.models.user import User  
from app.models.refresh_token import RefreshToken  
from app.models.api_usage import APIUsage  
from app.models.audit_log import AuditLog  
from app.models.rag_evaluation import RAGEvaluation  
from app.models.agent_execution import AgentExecution  # 👈 Registered your new agent telemetry table
from app.models.workspace import Workspace
from app.models.document import Document
from app.models.conversation import Conversation, Message


def create_tables():
    print("--- Verifying/Creating PostgreSQL Database Tables ---")
    Base.metadata.create_all(bind=engine)
    print("--- Database Tables Verified/Created Successfully ---")
