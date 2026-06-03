from uuid import uuid4
from sqlalchemy.orm import Session
from app.models.conversation import Conversation, Message


def create_conversation(db: Session, title: str):
    """
    Generates a fresh master session tracking row with a clean unique string hash.
    """
    conversation = Conversation(
        id=str(uuid4()),
        title=title
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def save_message(db: Session, conversation_id: str, role: str, content: str):
    """
    Saves individual user/assistant dialogue lines linked to a session.
    """
    message = Message(
        id=str(uuid4()),
        conversation_id=conversation_id,
        role=role,
        content=content
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_recent_messages(db: Session, conversation_id: str, limit: int = 10):
    """
    Retrieves chronological message history safely.
    """
    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
        .all()
    )

    # Reverse the descending data stream to feed the LLM accurate conversational order
    return list(reversed(messages))


def list_conversations(db: Session):
    """
    Retrieves all historical chat rooms for sidebar listing from newest to oldest.
    """
    return (
        db.query(Conversation)
        .order_by(Conversation.created_at.desc())
        .all()
    )


def get_conversation_detail(db: Session, conversation_id: str):
    """
    Fetches the master conversation details alongside all its linked historical messages.
    """
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        return None

    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )

    return {
        "conversation": conversation,
        "messages": messages
    }
