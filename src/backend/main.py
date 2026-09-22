
from src.backend.database.session import engine
from src.backend.constants import naming
from src.backend.dependencies.database import init_db, get_db
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from typing import Dict
from src.backend.routers.auth import router as auth_router
from src.backend.routers.user import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=naming.PROJECT_TITLE,
    description=naming.PROJECT_DESCRIPTION,
    version=naming.PROJECT_VERSION,
    lifespan=lifespan
)


@app.get("/", response_model=None, tags=["Root Route"])
async def read_root() -> Dict[str, str]:
    return {
        "message": f"Welcome to {naming.PROJECT_TITLE}"
    }


@app.get("/health", response_model=None, tags=["Health Route"])
async def health_check() -> Dict[str, str]:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "version": f"{naming.PROJECT_VERSION}"
        }
    except Exception:
        return {
            "status": "unhealthy",
            "version": f"{naming.PROJECT_VERSION}"
        }


app.include_router(
    router=auth_router,
    prefix=naming.MAIN_API_PREFIX
)


app.include_router(
    router=user_router,
    prefix=naming.MAIN_API_PREFIX
)
