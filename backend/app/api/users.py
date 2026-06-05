from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from app.db.dependencies import get_db
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.core.security import hash_password

router = APIRouter(
    prefix="/users",
    tags=["User Profile"]
)


# Pydantic Schema Model to filter secure output payloads
class UserProfileResponse(BaseModel):
    id: str
    email: EmailStr
    created_at: str

    class Config:
        from_attributes = True


# Pydantic Schema Model to validate profile updates securely
class UserProfileUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)


@router.get("/me", response_model=UserProfileResponse)
def get_user_profile(current_user: User = Depends(get_current_user)):
    """
    Retrieves the authenticated user's profile metadata details securely.
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at.isoformat()
    }


@router.patch("/me", response_model=UserProfileResponse)
def update_user_profile(
    payload: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Modifies account properties (email or password) for the authenticated multi-tenant user profile row.
    """
    # 1. Update the email address field if passed in the payload
    if payload.email is not None and payload.email != current_user.email:
        # Prevent email collisions across separate user entities
        existing_user = db.query(User).filter(User.email == payload.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This email address is already registered to another user profile account."
            )
        current_user.email = payload.email

    # 2. Update the encrypted password hash string block if passed
    if payload.password is not None:
        current_user.password_hash = hash_password(payload.password)

    try:
        db.commit()
        db.refresh(current_user)
        
        return {
            "id": current_user.id,
            "email": current_user.email,
            "created_at": current_user.created_at.isoformat()
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cleanly modify user account metadata: {str(e)}"
        )
