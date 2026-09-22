
from fastapi import HTTPException, status


INVALID_CREDENTIALS_EXCEPTIONS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid username or password."
)

INVALID_OR_EXPIRED_TOKEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or expired access token.",
    headers={"WWW-Authenticate": "Bearer"}
)


NOT_AUTHORIZED_FOR_ADMIN_ENDPOINTS_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You are not authorized to view this content."
)
