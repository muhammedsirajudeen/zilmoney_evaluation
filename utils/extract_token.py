from fastapi import HTTPException,status,Request


def get_token_from_header(request: Request) -> str:
    """
    Extract Bearer token from the Authorization header.
    
    :param request: FastAPI Request object
    :return: JWT token string
    """
    auth: str = request.headers.get("Authorization")
    if not auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    parts = auth.split()
    if parts[0].lower() != "bearer" or len(parts) != 2:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return parts[1]  # the token