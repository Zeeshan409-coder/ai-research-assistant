from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.services.memory_service import create_conversation, list_conversations, get_conversation_detail

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)


@router.post("/")
def create_new_conversation(db: Session = Depends(get_db)):
    conversation = create_conversation(db, "New Chat")
    return conversation


@router.get("/")
def get_all_conversations(db: Session = Depends(get_db)):
    return list_conversations(db)


@router.get("/{conversation_id}")
def get_conversation_room_detail(conversation_id: str, db: Session = Depends(get_db)):
    # 👈 Added Detail Route: Pulls the full history package or throws a 404 if missing
    detail = get_conversation_detail(db, conversation_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Conversation session not found")
    return detail
