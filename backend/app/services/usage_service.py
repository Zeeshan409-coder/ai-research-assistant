from uuid import uuid4
from sqlalchemy.orm import Session
from app.models.api_usage import APIUsage


def log_api_usage(db: Session, user_id: str, tokens: int = 0, is_retrieval: bool = False):
    """
    Metered Telemetry Logger: Safely tracks, registers, and increments individual SaaS accounts 
    request cycles, contextual token processing volumes, and vector database query scans.
    """
    try:
        # 1. Look look up an active analytics telemetry record row for this user
        record = db.query(APIUsage).filter(APIUsage.user_id == user_id).first()
        
        # 2. If no logging row exists yet for this profile, initialize a fresh one
        if not record:
            record = APIUsage(
                id=str(uuid4()),
                user_id=user_id,
                requests_count=1,
                tokens_consumed=tokens,
                retrieval_calls=1 if is_retrieval else 0
            )
            db.add(record)
        else:
            # 3. Otherwise, increment the structural metered usage counts cleanly
            record.requests_count += 1
            record.tokens_consumed += tokens
            if is_retrieval:
                record.retrieval_calls += 1
                
        db.commit()
        db.refresh(record)
        return record
        
    except Exception as e:
        db.rollback()
        print(f"--- Telemetry Logging Warning: Failed to write api usage logs: {e} ---")
        return None
