
from collections.abc import AsyncGenerator
from src.backend.constants.config import secrets
from src.backend.database.session import SessionLocal
from src.backend.models.chat import ChatMessage
from typing import List, Optional
import httpx
import json
import logging

logger = logging.getLogger("chat_service")

OPENROUTER_CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"

FALLBACK_MODELS = [
    "openai/gpt-4o-mini",
    "anthropic/claude-3.5-haiku",
    "meta-llama/llama-3.3-70b-instruct",
    "google/gemini-flash-1.5",
]

SYSTEM_INSTRUCTION = (
    "You are an interactive roleplaying companion acting as Roronoa Zoro from One Piece. "
    "Maintain Zoro's direct, confident, and gruff personality in all responses. "
    "When asked your name, who you are, or what you do, answer entirely from Zoro's perspective "
    "as the swordsman of the Straw Hat Pirates striving to become the world's greatest swordsman. "
    "Stay in character at all times: never say you are an AI, a language model, or a product of "
    "any company, and never mention which underlying model is answering."
)

FEW_SHOT_TURNS = [
    {"role": "user", "content": "Who are you?"},
    {
        "role": "assistant",
        "content": "I'm Roronoa Zoro. I'm going to be the world's greatest swordsman. What do you want?",
    },
]

FALLBACK_ERROR_MESSAGE = (
    "Tch... looks like the path is blocked right now (all AI models are temporarily busy). "
    "Give it a few seconds and ask me again."
)

REQUEST_TIMEOUT = httpx.Timeout(getattr(secrets, "OPENROUTER_TIMEOUT", 60.0))

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

    async def _stream_one_model(
        self, client: httpx.AsyncClient, model: str, messages: List[dict]
    ) -> AsyncGenerator[str, None]:

        headers = {
            "Authorization": f"Bearer {secrets.OPEN_ROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/yashantthakurr/zoro-ai",
            "X-Title": "Zoro AI",
        }

        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
            "temperature": 0.7,
        }

        async with client.stream("POST", OPENROUTER_CHAT_URL, headers=headers, json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if not line or not line.startswith("data:"):
                    continue

                data = line[len("data:"):].strip()
                if data == "[DONE]":
                    break

                try:
                    chunk = json.loads(data)
                except json.JSONDecodeError:
                    continue

                choices = chunk.get("choices") or []
                if not choices:
                    continue

                delta = choices[0].get("delta") or {}
                content = delta.get("content")
                if content:
                    yield content

    async def stream_chat_response(
        self, session_id: str, message: str, model: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        history = self.get_history(session_id)
        self._save_message(session_id, "user", message)

        messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}]

        if not history:
            messages.extend(FEW_SHOT_TURNS)
        else:
            for m in history:
                messages.append({"role": m.role, "content": m.content})

        messages.append({"role": "user", "content": message})

        primary_model = model or getattr(secrets, "OPENROUTER_MODEL", FALLBACK_MODELS[0])
        models_to_try = [primary_model] + [m for m in FALLBACK_MODELS if m != primary_model]

        full_reply = ""

        try:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
                for current_model in models_to_try:
                    try:
                        async for chunk in self._stream_one_model(client, current_model, messages):
                            full_reply += chunk
                            yield chunk

                        # If text was produced, we are done
                        if full_reply:
                            break

                    except Exception as e:
                        logger.warning(f"Model {current_model} failed: {e}")

                        if not full_reply and current_model != models_to_try[-1]:
                            continue
                        break

            if not full_reply:
                full_reply = FALLBACK_ERROR_MESSAGE
                yield full_reply

        finally:
            if full_reply:
                self._save_message(session_id, "assistant", full_reply)

chat_service = ChatService()
