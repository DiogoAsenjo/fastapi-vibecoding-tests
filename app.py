from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from database import engine, Base
from common.api_response import ApiResponse
from character.character_model import (
    CharacterModel,
)  # noqa: F401 — garante que o modelo é registrado
from character.router.character_router import router as character_router

# Cria as tabelas no banco (em produção, usar Alembic para migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Character CRUD", version="1.0.0")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Intercepta toda HTTPException e devolve no formato ApiResponse."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ApiResponse(message=exc.detail, data=None).model_dump(),
    )


app.include_router(character_router)
