
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
    if user.username != payload.session_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session ID and Username do not match.")
    return StreamingResponse(
        chat_service.stream_chat_response(
            session_id=payload.session_id,
            message=payload.message,
            model=payload.model,
        ),
        media_type="text/plain",
    )

@router.get("/history/{session_id}", response_model=ChatHistoryResponse)
def get_history(user: Annotated[User, Depends(get_current_user)], session_id: str, db: Session = Depends(get_db)) -> ChatHistoryResponse:
    if user.username != session_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session ID and Username do not match.")
    rows = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )
    return ChatHistoryResponse(
        session_id=session_id,
        messages=[ChatMessageOut.model_validate(r) for r in rows],
    )

@router.delete("/history/{session_id}")
def delete_history(user: Annotated[User, Depends(get_current_user)], session_id: str, db: Session = Depends(get_db)) -> Dict:
    if user.username != session_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session ID and Username do not match.")
    deleted = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .delete()
    )
    if not deleted:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No history found for this session.")
    db.commit()
    return {"status": "cleared", "session_id": session_id}
