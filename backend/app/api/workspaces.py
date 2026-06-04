from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.dependencies import get_db
from app.services import workspace_service

router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"]
)


class WorkspaceCreate(BaseModel):
    name: str


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_workspace(payload: WorkspaceCreate, db: Session = Depends(get_db)):
    """
    Initializes a completely isolated multi-document workspace container environment.
    """
    return workspace_service.create_workspace(db, name=payload.name)


@router.get("/")
def get_all_workspaces(db: Session = Depends(get_db)):
    """
    Lists all active enterprise-scoped workspace rows stored inside PostgreSQL.
    """
    return workspace_service.list_workspaces(db)


@router.get("/{workspace_id}")
def get_single_workspace_details(workspace_id: str, db: Session = Depends(get_db)):
    """
    Pulls structural metadata records for a single design workspace partition.
    """
    workspace = workspace_service.get_workspace(db, workspace_id=workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace room target profile not found")
    return workspace


@router.delete("/{workspace_id}")
def purge_workspace_container(workspace_id: str, db: Session = Depends(get_db)):
    """
    Permanently destroys a workspace container sandbox alongside all its relational dependencies.
    """
    success = workspace_service.delete_workspace(db, workspace_id=workspace_id)
    if not success:
        raise HTTPException(status_code=404, detail="Workspace target profile not found or already deleted")
    return {"status": "success", "message": "Workspace sandboxed environment and relational database entities fully purged."}


@router.get("/{workspace_id}/documents")
def get_workspace_documents_list(workspace_id: str, db: Session = Depends(get_db)):
    # 👈 Added Step 10 Route: Verifies the workspace exists first, then streams back its PDF log array
    workspace = workspace_service.get_workspace(db, workspace_id=workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Target workspace not found")
        
    return workspace_service.list_workspace_documents(db, workspace_id=workspace_id)

@router.get("/{workspace_id}/stats")
def get_workspace_dashboard_telemetry(workspace_id: str, db: Session = Depends(get_db)):
    """
    Provides rich analytics data (documents, conversations, chunks) to power the frontend metrics panels.
    """
    # Verify the workspace target folder exists first before aggregating parameters
    workspace = workspace_service.get_workspace(db, workspace_id=workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Target workspace not found")
        
    return workspace_service.get_workspace_analytics_stats(db, workspace_id=workspace_id)
