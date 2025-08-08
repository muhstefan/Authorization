import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from MyService.api_v1 import router as router_v1
from MyService.core.config import settings
from MyService.core.models import db_helper
from MyService.core.models.base import Base
from MyService.middleware.middleware import auth_middleware
from MyService.pages import router as pages_router

logger = logging.getLogger("uvicorn")


@asynccontextmanager  # контекстный менеджер в котором можно создать БД и что-то сделать после завершения
async def lifespan(app: FastAPI):
    async  with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Also accessible at: http://localhost:8000")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router_v1, prefix=settings.api_v1_prefix)
app.include_router(pages_router)
app.mount("/static", StaticFiles(directory="MyService/static"), name="static")
app.middleware("http")(auth_middleware)


@app.get("/")
async def root():
    return RedirectResponse(url="/pages/home")
