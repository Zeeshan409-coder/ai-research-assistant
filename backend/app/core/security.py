import bcrypt  # 👈 Drop passlib, leverage the native high-performance engine directly!


def hash_password(password: str) -> str:
    """
    Transforms a raw plain-text user password string into an irreversible 
    bcrypt salt-hashed token using native cryptographic primitives.
    """
    # Convert string characters into raw utf-8 bytes before salting
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Evaluates an inbound plain-text password entry against a stored database hash signature natively.
    """
    try:
        plain_bytes = plain_password.encode("utf-8")
        hashed_bytes = hashed_password.encode("utf-8")
        
        # Native byte-string checking prevents any internal truncation or compatibility faults
        return bcrypt.checkpw(plain_bytes, hashed_bytes)
    except Exception:
        return False
