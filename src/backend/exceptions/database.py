
from fastapi import HTTPException, status

DATABASE_UNHEALTHY_EXCEPTION = HTTPException(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail="unhealthy"
)
