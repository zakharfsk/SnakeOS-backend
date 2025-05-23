from fastapi import FastAPI
from contextlib import asynccontextmanager
from loguru import logger
from .auth import router as auth_router
from .system import router as system_router
from .docker import router as docker_router
from .settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    from . import connections

    logger.info(f"Starting up server '{app.title}'")
    await connections.init_external_clients(app)
    logger.info(f"Completed startup routines for '{app.title}'")

    yield

    await connections.shutdown()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan,
    swagger_ui_parameters={
        "persistAuthorization": True,
        "displayRequestDuration": True,
        "filter": True,
    },
)

# Register routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(system_router, prefix=settings.API_V1_STR)
app.include_router(docker_router, prefix=settings.API_V1_STR)
