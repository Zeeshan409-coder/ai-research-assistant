from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.user import User
from app.models.workspace import Workspace
from app.dependencies.auth import get_current_user
from app.schemas.research import ResearchRequest
from app.orchestration.research_orchestrator import ResearchOrchestrator

router = APIRouter(
    prefix="/research",
    tags=["Agentic Research Workflows"]
)

# Instantiate a single shared orchestrator manager engine
orchestrator = ResearchOrchestrator()


@router.post("", status_code=status.HTTP_200_OK)
async def run_research_workflow(
    request: ResearchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Agentic Gateway: Validates tenant sandbox permissions and boots up a top-down,
    deterministic automated multi-agent research and context compilation workflow loop.
    """
    # 🛡️ Multi-Tenant Firewall Guard: Cross-examine ownership bounds before releasing agents
    workspace = db.query(Workspace).filter(Workspace.id == request.workspace_id).first()
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The targeted workspace container could not be located."
        )
        
    if workspace.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You do not possess structural ownership clearances for this workspace sandbox room."
        )

    try:
        # Trigger the asynchronous top-down orchestration pipeline execution matrix
        result = await orchestrator.execute(
            workspace_id=request.workspace_id,
            query=request.query
        )
        
        # Inject additional session contextual identifiers to match frontend state needs
        return {
            "status": "success",
            "workspace_id": request.workspace_id,
            "conversation_id": request.conversation_id,
            **result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agentic orchestration framework faulted during active loop execution: {str(e)}"
        )
