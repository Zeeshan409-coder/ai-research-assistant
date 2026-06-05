import jwt
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.user import User
from app.core.auth import SECRET_KEY, ALGORITHM


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """
    Security Firewall: Direct Header Token Extractor. 
    Decodes standard 'Authorization: Bearer <token>' headers natively 
    without being locked into restrictive OAuth2 form parsing classes.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials or active session has expired.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 1. Extract the raw Authorization header out of the request tracking variables
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise credentials_exception

    try:
        # 2. Split the 'Bearer <token>' string packet layout cleanly
        token_type, token = auth_header.split(" ")
        if token_type.lower() != "bearer":
            raise credentials_exception
            
        # 3. Cryptographically decode and verify the token signature using PyJWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # 4. Extract the user identifier from the Subject (sub) claim
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
    except (ValueError, jwt.PyJWTError):
        raise credentials_exception

    # 5. Pull the matching user account row directly out of PostgreSQL database memory
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    # 6. Return the live authenticated database record object natively to your endpoints
    return user
