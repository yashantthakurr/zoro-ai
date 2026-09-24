import logging
from collections.abc import AsyncGenerator
from typing import List, Optional

from google import genai
from google.genai import types

from src.backend.constants.config import secrets
from src.backend.database.session import SessionLocal
from src.backend.models.chat import ChatMessage

logger = logging.getLogger("chat_service")
ai_client = genai.Client(api_key=secrets.GEMINI_API_KEY)

# Active production models from your supported key list in priority order
FALLBACK_MODELS = [
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash",
]

SYSTEM_INSTRUCTION = (
    "You are an interactive roleplaying companion acting as Roronoa Zoro from One Piece. "
    "Maintain Zoro's direct, confident, and gruff personality in all responses. "
    "When asked your name, who you are, or what you do, answer entirely from Zoro's perspective "
    "as the swordsman of the Straw Hat Pirates striving to become the world's greatest swordsman."
)

FEW_SHOT_TURNS = [
    {"role": "user", "parts": [{"text": "Who are you?"}]},
    {
        "role": "model",
        "parts": [
            {
                "text": "I'm Roronoa Zoro. I'm going to be the world's greatest swordsman. What do you want?"
            }
        ],
    },
]

FALLBACK_ERROR_MESSAGE = (
    "Tch... looks like the path is blocked right now (all AI models are temporarily busy). "
    "Give it a few seconds and ask me again."
)


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

        gemini_contents = []
        if not history:
            gemini_contents.extend(FEW_SHOT_TURNS)
        else:
            for m in history:
                gemini_contents.append(
                    {
                        "role": "model" if m.role == "assistant" else "user",
                        "parts": [{"text": m.content}],
                    }
                )

        gemini_contents.append({"role": "user", "parts": [{"text": message}]})

        primary_model = model or getattr(secrets, "GEMINI_MODEL", "gemini-3.7-flash")
        models_to_try = [primary_model] + [m for m in FALLBACK_MODELS if m != primary_model]

        generation_config = types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.7,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            ),
        )

        full_reply = ""

        try:
            for current_model in models_to_try:
                try:
                    response = await ai_client.aio.models.generate_content_stream(
                        model=current_model,
                        contents=gemini_contents,
                        config=generation_config,
                    )
                    async for chunk in response:
                        if chunk.text:
                            full_reply += chunk.text
                            yield chunk.text

                    # If text was produced, we are done
                    if full_reply:
                        break

                except Exception as e:
                    logger.warning(f"Model {current_model} failed: {e}")

                    # If no output was yielded yet, continue to the next model
                    if not full_reply and current_model != models_to_try[-1]:
                        continue
                    break

            # Guarantee that a response is always emitted
            if not full_reply:
                full_reply = FALLBACK_ERROR_MESSAGE
                yield full_reply

        finally:
            if full_reply:
                self._save_message(session_id, "assistant", full_reply)


chat_service = ChatService()