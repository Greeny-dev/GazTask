from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from . import dependency

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)


    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi"):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        is_valid = await dependency.auth_service.check(auth_header)

        if not is_valid:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid or missing Basic authentication"},
                headers={"WWW-Authenticate": "Basic"},
            )

        return await call_next(request)
