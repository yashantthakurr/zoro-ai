
import json
from collections.abc import AsyncGenerator
from typing import Optional, List

import httpx

from src.backend.constants.config import secrets
from src.backend.database.session import SessionLocal
from src.backend.models.chat import ChatMessage

GROQ_CHAT_COMPLETIONS_URL = "https://api.groq.com/openai/v1/chat/completions"


class ChatService:

    def get_history(self, session_id: str) -> List[ChatMessage]:
        db = SessionLocal()
        try:
            return (
                db.query(ChatMessage)
                .filter(ChatMessage.session_id == session_id)
                .order_by(ChatMessage.created_at.asc())
                .all()
            )
        finally:
            db.close()

    def _save_message(self, session_id: str, role: str, content: str) -> None:
        db = SessionLocal()
        try:
            db.add(ChatMessage(session_id=session_id, role=role, content=content))
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def clear_history(self, session_id: str) -> int:
        db = SessionLocal()
        try:
            deleted = (
                db.query(ChatMessage)
                .filter(ChatMessage.session_id == session_id)
                .delete()
            )
            db.commit()
            return deleted
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    async def stream_chat_response(
        self, session_id: str, message: str, model: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        history = self.get_history(session_id)
        self._save_message(session_id, "user", message)

        groq_messages = [{"role": m.role, "content": m.content} for m in history]
        groq_messages.append({"role": "user", "content": message})

        payload = {
            "model": model or secrets.GROQ_MODEL,
            "messages": groq_messages,
            "stream": True,
        }
        headers = {
            "Authorization": f"Bearer {secrets.GROQ_API_KEY}",
            "Content-Type": "application/json",
        }

        full_reply = ""

        try:
            async with httpx.AsyncClient(timeout=secrets.GROQ_TIMEOUT) as client:
                async with client.stream(
                    "POST", GROQ_CHAT_COMPLETIONS_URL, json=payload, headers=headers
                ) as response:
                    if response.status_code >= 400:
                        error_body = (await response.aread()).decode(errors="replace")
                        error_msg = (error_body)
                        full_reply += error_msg
                        yield error_msg
                        return

                    async for line in response.aiter_lines():
                        if not line or not line.startswith("data: "):
                            continue
                        data = line[len("data: ") :].strip()
                        if data == "[DONE]":
                            break
                        chunk = json.loads(data)
                        piece = chunk["choices"][0]["delta"].get("content", "")
                        if piece:
                            full_reply += piece
                            yield piece
        except httpx.ConnectError:
            error_msg = "\n[Error: could not reach the Groq API. Check your network/API key.]"
            full_reply += error_msg
            yield error_msg
        finally:
            if full_reply:
                self._save_message(session_id, "assistant", full_reply)


chat_service = ChatService()
