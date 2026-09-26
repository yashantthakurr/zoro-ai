
from datetime import datetime
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field
)
from typing import Optional

class UserSignup(BaseModel):

    email: EmailStr = Field(..., max_length=254)
    username: str = Field(..., min_length=4, max_length=24)
    password: str = Field(..., min_length=8, max_length=64)

class UserSignin(BaseModel):

    username: str = Field(..., min_length=4, max_length=24)
    password: str = Field(..., min_length=8, max_length=64)

class UserUpdate(BaseModel):

    email: Optional[EmailStr] = Field(None, max_length=254)
    username: Optional[str] = Field(None, min_length=4, max_length=24)
    new_password: Optional[str] = Field(None, min_length=8, max_length=64)
    current_password: Optional[str] = Field(..., min_length=8, max_length=64)

class UserResponse(BaseModel):

    id: int
    email: EmailStr
    username: str
    role: str
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
