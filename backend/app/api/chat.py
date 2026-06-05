from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.user import User
from app.models.workspace import Workspace  # 👈 Imported workspace model for ownership validation
from app.dependencies.auth import get_current_user  # 👈 Enforces JWT validation
from app.services.hybrid_service import hybrid_search
from app.services.prompt_service import build_prompt
from app.services.llm_service import generate_response
from app.services.retrieval_metrics import calculate_context_stats
from app.services.memory_service import get_recent_messages, save_message

router = APIRouter()


class ChatRequest(BaseModel):
    workspace_id: str     
    conversation_id: str  
    query: str


@router.post("/chat")
async def chat(
    request: ChatRequest, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 👈 Locked endpoint behind auth guard
):
    # 🛡️ 1. RETRIEVAL SECURITY LAYER: Verify the workspace exists and belongs to this user
    workspace = db.query(Workspace).filter(Workspace.id == request.workspace_id).first()
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="The targeted research workspace could not be found."
        )
        
    if workspace.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You do not possess retrieval permissions for this workspace folder context."
        )

    # 2. Pull the chronological chat room log history right out of PostgreSQL memory
    history = get_recent_messages(
        db=db,
        conversation_id=request.conversation_id,
        limit=10
    )

    # 3. Run the multi-stage Hybrid Retrieval + Neural Cross-Encoder Reranker
    search_results = hybrid_search(
        query=request.query,
        workspace_id=request.workspace_id,
        top_k=5
    )

    # 4. Compress context blocks cleanly below the 8000-character ceiling
    prompt, used_results = build_prompt(
        query=request.query,
        search_results=search_results,
        history=history,
        max_chars=8000
    )

    # 5. Process analytics metrics on the compressed chunk payload
    context_stats = calculate_context_stats(used_results)

    # 6. Generate high-precision answer from your local model
    answer = generate_response(prompt)

    # 7. Commit both dialogue tracks straight back to PostgreSQL memory
    save_message(db=db, conversation_id=request.conversation_id, role="user", content=request.query)
    save_message(db=db, conversation_id=request.conversation_id, role="assistant", content=answer)

    citations = []
    for result in used_results:
        citations.append({
            "source": result["metadata"]["source"],
            "page_number": result["metadata"]["page_number"],
            "chunk_index": result["metadata"]["chunk_index"],
            "rerank_score": result["rerank_score"]
        })

    return {
        "workspace_id": request.workspace_id,
        "conversation_id": request.conversation_id,
        "query": request.query,
        "answer": answer,
        "metrics": context_stats,
        "citations": citations
    }
