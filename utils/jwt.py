from datetime import datetime, timedelta
import jwt  # PyJWT

# Secret key (keep this safe!)
SECRET_KEY = "your_super_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT token with optional expiration.
    
    :param data: dict containing payload (e.g., {"user_id": 1})
    :param expires_delta: optional timedelta for token expiry
    :return: encoded JWT string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


import jwt
from jwt import PyJWTError

SECRET_KEY = "your_super_secret_key"  # same as used for encoding
ALGORITHM = "HS256"

def decode_access_token(token: str):
    """
    Decode a JWT token and return the payload.
    Raises exception if token is invalid or expired.
    
    :param token: JWT string
    :return: dict payload
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError as e:
        raise ValueError(f"Invalid or expired token: {str(e)}")