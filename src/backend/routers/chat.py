
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from src.backend.constants.naming import CHAT_API_PREFIX
from src.backend.dependencies.auth import get_current_user
from src.backend.dependencies.database import get_db
from src.backend.models import User
from src.backend.models.chat import ChatMessage
from src.backend.schemas.chat import ChatHistoryResponse, ChatMessageOut, ChatRequest
from src.backend.services.chat import chat_service
from sqlalchemy.orm import Session
from typing import Annotated, Dict

router = APIRouter(prefix=CHAT_API_PREFIX, tags=["Chat Routes"])

@router.post("/send")
async def send_message(payload: ChatRequest, user: Annotated[User, Depends(get_current_user)]) -> StreamingResponse:
    return StreamingResponse(
        chat_service.stream_chat_response(
            user_id=user.id,
            message=payload.message,
        ),
        media_type="text/plain",
    )

@router.get("/history", response_model=ChatHistoryResponse)
def get_history(user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)) -> ChatHistoryResponse:
    rows = (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == user.id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )
    return ChatHistoryResponse(messages=[ChatMessageOut.model_validate(r) for r in rows])

@router.delete("/history")
def delete_history(user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)) -> Dict[str, str]:
    deleted = (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == user.id)
        .delete()
    )
    if not deleted:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No history found.")
    db.commit()
    return {"status": "cleared"}
