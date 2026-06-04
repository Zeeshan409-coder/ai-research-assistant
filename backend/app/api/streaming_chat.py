import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.services.hybrid_service import hybrid_search
from app.services.prompt_service import build_prompt
from app.services.retrieval_metrics import calculate_context_stats
from app.services.memory_service import get_recent_messages, save_message
from app.services.streaming_llm_service import stream_response

router = APIRouter()


class StreamRequest(BaseModel):
    workspace_id: str      # 👈 Enforces total data partitioning constraint check
    conversation_id: str   # Mandatory historical room session tracker key
    query: str


@router.post("/chat/stream")
async def stream_chat(request: StreamRequest, db: Session = Depends(get_db)):
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

    # 4. Calculate analytics metrics on the compressed chunk payload
    context_stats = calculate_context_stats(used_results)

    # 5. Extract citations exclusively for chunks that passed compression filtering
    citations = []
    for result in used_results:
        citations.append({
            "source": result["metadata"]["source"],
            "page_number": result["metadata"]["page_number"],
            "chunk_index": result["metadata"]["chunk_index"],
            "rerank_score": result["rerank_score"]
        })

    # 6. Build the asynchronous generator wrapper to pipe data over SSE protocols safely
    async def event_generator():
        # First event: Send your rich search citations and token payload stats instantly under metadata type
        initial_payload = {
            "type": "metadata",
            "metrics": context_stats,
            "citations": citations
        }
        yield f"data: {json.dumps(initial_payload)}\n\n"

        full_assistant_response = ""

        # Loop through every individual word token generated locally by your Llama model
        async for token in stream_response(prompt):
            full_assistant_response += token
            
            # Formatted SSE Event: Wrap token chunks under explicit "token" type flag
            token_payload = {
                "type": "token",
                "content": token
            }
            yield f"data: {json.dumps(token_payload)}\n\n"

        # Final SSE Event: Signal the frontend client that the network stream has safely finished
        done_payload = {"type": "done"}
        yield f"data: {json.dumps(done_payload)}\n\n"

        # Save both dialogue tracks to PostgreSQL once the stream finishes successfully
        save_message(db=db, conversation_id=request.conversation_id, role="user", content=request.query)
        save_message(db=db, conversation_id=request.conversation_id, role="assistant", content=full_assistant_response)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
