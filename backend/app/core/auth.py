import os
from datetime import datetime, timedelta, timezone
import jwt  # 👈 Using the high-performance PyJWT library natively

# Environmental configuration mappings with secure fallback parameters
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "7b9d5c8e2a4f13579bcfad0123456789abcdef0123456789abcdef0123456789")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Encodes and signs a secure JSON Web Token payload containing user identity parameters.
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    # Append the expiration timestamp claim natively into the token bundle
    to_encode.update({"exp": expire})
    
    # Sign and output the final encrypted token text string
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
