from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.dependencies import get_db
from app.models.user import User  
from app.dependencies.auth import get_current_user  
from app.services import workspace_service

router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"]
)


class WorkspaceCreate(BaseModel):
    name: str


# 🎯 FIXED: Changed path descriptor from "/" to "" to prevent header-stripping 307 redirects
@router.post("", status_code=status.HTTP_201_CREATED)
def create_new_workspace(
    payload: WorkspaceCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  
):
    """
    Initializes a completely isolated multi-document workspace container environment
    owned explicitly by the authenticated multi-user SaaS account owner.
    """
    workspace = workspace_service.create_workspace(db, name=payload.name)
    workspace.owner_id = current_user.id
    db.commit()
    db.refresh(workspace)
    return workspace


@router.get("")
def get_all_workspaces(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  
):
    """
    Lists all enterprise-scoped workspaces owned exclusively by the authenticated user account profile.
    """
    return db.query(workspace_service.Workspace).filter(workspace_service.Workspace.owner_id == current_user.id).all()


@router.get("/{workspace_id}")
def get_single_workspace_details(
    workspace_id: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Pulls structural metadata records for a single workspace partition, verifying account ownership stakes.
    """
    workspace = workspace_service.get_workspace(db, workspace_id=workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace room target profile not found")
    
    if workspace.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied: You do not possess ownership permissions for this workspace partition.")
        
    return workspace


@router.delete("/{workspace_id}")
def purge_workspace_container(
    workspace_id: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Permanently destroys a workspace container sandbox alongside all its relational dependencies.
    """
    workspace = workspace_service.get_workspace(db, workspace_id=workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace target profile not found or already deleted")
        
    if workspace.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied: Relational database entity purge restricted to account owners.")
        
    workspace_service.delete_workspace(db, workspace_id=workspace_id)
    return {"status": "success", "message": "Workspace sandboxed environment and relational database entities fully purged."}


@router.get("/{workspace_id}/documents")
def get_workspace_documents_list(
    workspace_id: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Streams back the complete uploaded PDF tracker logs sub-array for a designated workspace silo.
    """
    workspace = workspace_service.get_workspace(db, workspace_id=workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Target workspace not found")
        
    if workspace.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied: Ingestion manifest logs restricted to account owners.")
        
    return workspace_service.list_workspace_documents(db, workspace_id=workspace_id)


@router.get("/{workspace_id}/stats")
def get_workspace_dashboard_telemetry(
    workspace_id: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Provides rich analytics data (documents, conversations, chunks) to power the frontend metrics panels.
    """
    workspace = workspace_service.get_workspace(db, workspace_id=workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Target workspace not found")
        
    if workspace.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied: Telemetry statistics profiles restricted to account owners.")
        
    return workspace_service.get_workspace_analytics_stats(db, workspace_id=workspace_id)
