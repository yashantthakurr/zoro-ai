
from src.backend.constants.config import secrets
from datetime import datetime , timedelta, timezone
from pwdlib import PasswordHash
from jose import jwt
from uuid import uuid4

password_hash = PasswordHash.recommended()


def hash_password(plain_password: str) -> str:
    return password_hash.hash(plain_password)


def verify_passowrd(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def generate_access_token(username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {"subject": username, "exp": expire, "jwtid": str(uuid4())}
    return jwt.encode(payload, algorithm=secrets.ALGORITHM, key=secrets.SECRET_KEY)
