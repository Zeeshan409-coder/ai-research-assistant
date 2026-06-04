from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.services.hybrid_service import hybrid_search
from app.services.prompt_service import build_prompt
from app.services.llm_service import generate_response
from app.services.retrieval_metrics import calculate_context_stats
from app.services.memory_service import get_recent_messages, save_message

router = APIRouter()


class ChatRequest(BaseModel):
    workspace_id: str     # 👈 Enforces matching workspace folder isolation scope lookup
    conversation_id: str  # Mandatory historical room session parameter
    query: str


@router.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    # 1. Pull the chronological chat room log history right out of PostgreSQL memory
    history = get_recent_messages(
        db=db,
        conversation_id=request.conversation_id,
        limit=10
    )

    # 2. Run the multi-stage Hybrid Retrieval + Neural Cross-Encoder Reranker
    # Enforces workspace isolation directly inside the vector search pipeline
    search_results = hybrid_search(
        query=request.query,
        workspace_id=request.workspace_id,
        top_k=5
    )

    # 3. Compress context blocks cleanly below the 8000-character ceiling
    prompt, used_results = build_prompt(
        query=request.query,
        search_results=search_results,
        history=history,
        max_chars=8000
    )

    # 4. Process analytics metrics on the compressed chunk payload
    context_stats = calculate_context_stats(used_results)

    # 5. Generate high-precision answer from your local local model
    answer = generate_response(prompt)

    # 6. Commit both dialogue tracks straight back to PostgreSQL memory
    save_message(db=db, conversation_id=request.conversation_id, role="user", content=request.query)
    save_message(db=db, conversation_id=request.conversation_id, role="assistant", content=answer)

    citations = []
    # 7. Extract citations exclusively for chunks that passed compression filtering
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
