
from contextlib import asynccontextmanager
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from src.backend.constants import naming
from src.backend.constants.config import secrets
from src.backend.database.session import engine
from src.backend.dependencies.database import init_db
from src.backend.dependencies.rate_limit import limiter
from src.backend.exceptions.database import DATABASE_UNHEALTHY_EXCEPTION
from src.backend.routers.auth import router as auth_router
from src.backend.routers.chat import router as chat_router
from src.backend.routers.user import router as user_router
from sqlalchemy import text
from typing import Dict

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title=naming.PROJECT_TITLE,
    description=naming.PROJECT_DESCRIPTION,
    version=naming.PROJECT_VERSION,
    lifespan=lifespan,
    docs_url="/docs" if secrets.DEBUG else None,
    redoc_url="/redoc" if secrets.DEBUG else None,
    openapi_url="/openapi.json" if secrets.DEBUG else None
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/", response_model=None, tags=["Public Routes"])
async def read_root() -> Dict[str, str]:
    return {
        "message": f"Welcome to {naming.PROJECT_TITLE}"
    }

@app.get("/health", response_model=None, tags=["Public Routes"])
async def health_check() -> Dict[str, str]:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "version": f"{naming.PROJECT_VERSION}"
        }
    except Exception:
        raise DATABASE_UNHEALTHY_EXCEPTION

app.include_router(
    router=auth_router,
    prefix=naming.MAIN_API_PREFIX
)

app.include_router(
    router=user_router,
    prefix=naming.MAIN_API_PREFIX
)

app.include_router(
    router=chat_router,
    prefix=naming.MAIN_API_PREFIX
)
