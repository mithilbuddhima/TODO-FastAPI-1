from fastapi import Request, HTTPException
from jose import JWTError
from app.auth.jwt import verify_token as decode_and_validate 

def verify_token(request: Request):
    """FastAPI dependency that returns the current user if the JWT is valid."""
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

    token = auth.split(" ", 1)[1].strip()

    try:
        current_user = decode_and_validate(token) 
        return current_user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")