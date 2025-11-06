from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

ALLOWED_PATHS = {"/docs", "/openapi.json", "/register", "/token"}

class TokenVerificationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ALLOWED_PATHS:   
            return await call_next(request)

        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=401, detail="Authorization token is missing")

        return await call_next(request)