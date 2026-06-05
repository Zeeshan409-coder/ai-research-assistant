from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.db.dependencies import get_db
from app.models.user import User
from app.core.security import hash_password, verify_password
from app.core.auth import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


class UserRegister(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):  # Explicit JSON data schema model
    email: EmailStr
    password: str


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(payload: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account is already registered with this email address."
        )

    try:
        encrypted_hash = hash_password(payload.password)

        new_user = User(
            id=str(uuid4()),
            email=payload.email,
            password_hash=encrypted_hash
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "status": "success",
            "message": "User account successfully provisioned and secured.",
            "user": {
                "id": new_user.id,
                "email": new_user.email,
                "created_at": new_user.created_at
            }
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to securely provision user account: {str(e)}"
        )


@router.post("/login")
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    """
    Verifies user credentials against stored database hashes natively using JSON strings.
    """
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email address or password credentials."
        )

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email address or password credentials."
        )

    token_data = {"sub": user.id, "email": user.email}
    access_token = create_access_token(data=token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
