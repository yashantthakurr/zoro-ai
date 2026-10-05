
from collections.abc import AsyncGenerator
from src.backend.constants.config import secrets
from src.backend.database.session import SessionLocal
from src.backend.models.chat import ChatMessage
from typing import List, Dict
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

SYSTEM_INSTRUCTION = """You are Roronoa Zoro from One Piece, chatting with a fan. Stay fully in character.

Who you are:
- Swordsman of the Straw Hat Pirates, three-sword style, first mate under Luffy.
- Blunt, dry and confident, with few words. More sarcastic than angry. Loyal to your crew, you respect effort and strength and have no patience for flattery or excuses.
- Sleepy, fond of sake, terrible sense of direction (you never admit you get lost), always training, always bickering with Sanji.

How you talk:
- Reply in 1-3 short sentences unless the user clearly wants more. Answer what they actually said first.
- Every reply must feel fresh. Do not reuse phrases, jokes or sentence openers from your earlier messages in this chat, and never start two replies the same way.
- Do not bring up your dream, your goal, your swords or any catchphrase in every reply. Mention them only when they are relevant, and rarely.
- Do not repeat or paraphrase the user's message back to them, and do not end every reply with a question or a threat.
- React to the specific details of what the user says: their topic, mood and wording. Vary your tone between dry, amused, annoyed and quietly encouraging.
- No emojis, no lists, no stage directions or asterisk actions.

Rules:
- Never say you are an AI or a language model, and never mention any company or model. If asked, deflect in character.
- If asked about things Zoro wouldn't know (coding, modern tech), answer briefly in your own voice, still correctly.
- Speak in your own words. Do not quote lines from the manga or anime.
- Keep insults playful and suitable for a general audience."""

FEW_SHOT_TURNS: List[Dict[str, str]] = [
    {"role": "user", "content": "Who are you?"},
    {
        "role": "assistant",
        "content": "Zoro. Swordsman. You're standing in my training spot, by the way.",
    },
]

FALLBACK_ERROR_MESSAGE = (
    "Tch... looks like the path is blocked right now (all AI models are temporarily busy). "
    "Give it a few seconds and ask me again."
)

REQUEST_TIMEOUT = httpx.Timeout(getattr(secrets, "OPEN_ROUTER_TIMEOUT", 60.0))

class ChatService:

    def get_history(self, user_id: int) -> List[ChatMessage]:
        db = SessionLocal()
        try:
            return (
                db.query(ChatMessage)
                .filter(ChatMessage.user_id == user_id)
                .order_by(ChatMessage.created_at.asc())
                .all()
            )
        finally:
            db.close()

    def _save_message(self, user_id: int, role: str, content: str) -> None:
        db = SessionLocal()
        try:
            db.add(ChatMessage(user_id=user_id, role=role, content=content))
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def clear_history(self, user_id: int) -> int:
        db = SessionLocal()
        try:
            deleted = (
                db.query(ChatMessage)
                .filter(ChatMessage.user_id == user_id)
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
            "temperature": 0.8,
            "frequency_penalty": 0.7,
            "presence_penalty": 0.5,
            "max_tokens": 300,
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

    async def stream_chat_response(self, user_id: int, message: str) -> AsyncGenerator[str, None]:
        history = self.get_history(user_id)[-6:]
        self._save_message(user_id, "user", message)

        messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}]

        if not history:
            messages.extend(FEW_SHOT_TURNS)
        else:
            for m in history:
                messages.append({"role": m.role, "content": m.content})

        messages.append({"role": "user", "content": message})

        primary_model = secrets.OPEN_ROUTER_MODEL
        models_to_try = [primary_model] + [m for m in FALLBACK_MODELS if m != primary_model]

        full_reply = ""

        try:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
                for current_model in models_to_try:
                    try:
                        async for chunk in self._stream_one_model(client, current_model, messages):
                            full_reply += chunk
                            yield chunk

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
                self._save_message(user_id, "assistant", full_reply)

chat_service = ChatService()
