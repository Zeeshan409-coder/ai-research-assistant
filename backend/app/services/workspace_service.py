from uuid import uuid4
from sqlalchemy.orm import Session
from app.models.workspace import Workspace
from app.models.document import Document
from sqlalchemy import func
from app.models.conversation import Conversation
from app.models.document import Document


def create_workspace(db: Session, name: str) -> Workspace:
    """
    Initializes an isolated research workspace sandbox inside PostgreSQL.
    """
    workspace = Workspace(
        id=str(uuid4()),
        name=name
    )
    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    return workspace


def get_workspace(db: Session, workspace_id: str) -> Workspace:
    """
    Retrieves the master metadata details for a specific workspace container.
    """
    return db.query(Workspace).filter(Workspace.id == workspace_id).first()


def list_workspaces(db: Session) -> list[Workspace]:
    """
    Fetches every active production-grade workspace silo on the platform.
    """
    return db.query(Workspace).order_by(Workspace.created_at.desc()).all()


def delete_workspace(db: Session, workspace_id: str) -> bool:
    """
    Deletes a workspace. Relational cascade rules automatically drop
    all linked documents, chat sessions, and history logs inside PostgreSQL.
    """
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    if not workspace:
        return False
        
    db.delete(workspace)
    db.commit()
    return True


# 👈 Appended Step 10 Logic: Fetches all tracked PDF metadata entries for a single workspace
def list_workspace_documents(db: Session, workspace_id: str) -> list[Document]:
    """
    Queries and returns all tracking documents uploaded to a specific workspace silo.
    """
    return db.query(Document).filter(Document.workspace_id == workspace_id).order_by(Document.uploaded_at.desc()).all()


def get_workspace_analytics_stats(db: Session, workspace_id: str) -> dict:
    """
    Runs lightning-fast database aggregations to compile dashboard telemetry data.
    """
    # 1. Count total unique files registered in this specific workspace room
    total_docs = db.query(Document).filter(Document.workspace_id == workspace_id).count()
    
    # 2. Count total conversation session paths tied to this workspace
    total_convs = db.query(Conversation).filter(Conversation.workspace_id == workspace_id).count()
    
    # 3. Sum total chunk partitions compiled across all workspace documents safely
    total_chunks_result = db.query(func.sum(Document.total_chunks))\
                            .filter(Document.workspace_id == workspace_id)\
                            .scalar()
    
    # Clean fallback default if no documents are uploaded yet
    total_chunks = int(total_chunks_result) if total_chunks_result is not None else 0

    return {
        "documents": total_docs,
        "conversations": total_convs,
        "chunks": total_chunks
    }
