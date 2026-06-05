from uuid import uuid4
from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog


def create_audit_entry(
    db: Session, 
    user_id: str, 
    action: str, 
    resource_type: str, 
    resource_id: str = None, 
    details: str = None,
    ip_address: str = None
):
    """
    Compliance Engine: Safely stamps, seals, and records security-relevant enterprise events 
    directly into your PostgreSQL immutable log ledger.
    """
    try:
        new_log = AuditLog(
            id=str(uuid4()),
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address
        )
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        return new_log
    except Exception as e:
        db.rollback()
        print(f"--- Enterprise Audit Warning: Failed to write system security log: {e} ---")
        return None
