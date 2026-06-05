import json
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.user import User
from app.models.workspace import Workspace  # 👈 Imported workspace model for ownership cross-checking
from app.dependencies.auth import get_current_user  # 👈 Enforces JWT validation
from app.services.hybrid_service import hybrid_search
from app.services.prompt_service import build_prompt
from app.services.retrieval_metrics import calculate_context_stats
from app.services.memory_service import get_recent_messages, save_message
from app.services.streaming_llm_service import stream_response

router = APIRouter()


class StreamRequest(BaseModel):
    workspace_id: str      
    conversation_id: str   
    query: str


@router.post("/chat/stream")
async def stream_chat(
    request: StreamRequest, 
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

    # 5. Calculate analytics metrics on the compressed chunk payload
    context_stats = calculate_context_stats(used_results)

    # 6. Extract citations exclusively for chunks that passed compression filtering
    citations = []
    for result in used_results:
        citations.append({
            "source": result["metadata"]["source"],
            "page_number": result["metadata"]["page_number"],
            "chunk_index": result["metadata"]["chunk_index"],
            "rerank_score": result["rerank_score"]
        })

    # 7. Build the asynchronous generator wrapper to pipe data over SSE protocols safely
    async def event_generator():
        initial_payload = {
            "type": "metadata",
            "metrics": context_stats,
            "citations": citations
        }
        yield f"data: {json.dumps(initial_payload)}\n\n"

        full_assistant_response = ""

        async for token in stream_response(prompt):
            full_assistant_response += token
            token_payload = {
                "type": "token",
                "content": token
            }
            yield f"data: {json.dumps(token_payload)}\n\n"

        done_payload = {"type": "done"}
        yield f"data: {json.dumps(done_payload)}\n\n"

        # Save both dialogue tracks to PostgreSQL once the stream finishes successfully
        save_message(db=db, conversation_id=request.conversation_id, role="user", content=request.query)
        save_message(db=db, conversation_id=request.conversation_id, role="assistant", content=full_assistant_response)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
