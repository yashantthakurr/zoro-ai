
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Literal

class ChatMessageOut(BaseModel):

    role: Literal["user", "assistant"]
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ChatRequest(BaseModel):

    session_id: str = Field(...)
    message: str = Field(..., min_length=1, max_length=3000)

class ChatHistoryResponse(BaseModel):

    session_id: str
    messages: List[ChatMessageOut]
