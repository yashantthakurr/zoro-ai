
from fastapi import HTTPException, status

EMAIL_ALREADY_TAKEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User with the provided email already exists. Try with some another email."
)

USERNAME_ALREADY_TAKEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User with the provided username already exists. Try with some another username."
)

CANNOT_FIND_USER_WITH_ID_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Cannot find any user with the provided ID."
)
