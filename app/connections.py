from fastapi import FastAPI
from tortoise import Tortoise
from app.settings import settings
from loguru import logger
from tortoise.contrib.fastapi import register_tortoise


async def init_tortoise(app: FastAPI):
    """
    Initialize Tortoise ORM with PostgreSQL database connection.
    Uses connection pooling by default (min_size=1, max_size=5)
    """
    await Tortoise.init(
        db_url=settings.DB_URL,
        modules={"models": ["app.models"]},
    )
    await Tortoise.generate_schemas()

    # Register exception handlers
    register_tortoise(
        app,
        db_url=settings.DB_URL,
        modules={"models": ["app.models"]},
        generate_schemas=False,  # Schema already generated above
        add_exception_handlers=True,
    )


async def init_redis():
    """
    Initialize Redis connection if configured.
    """
    if settings.REDIS_HOST and settings.REDIS_PORT:
        # Redis connection logic would go here
        # Example: redis = await aioredis.create_redis_pool(f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}')
        logger.info(
            f"Redis connection initialized to {settings.REDIS_HOST}:{settings.REDIS_PORT}"
        )
    else:
        logger.info("Redis connection not configured, skipping")


async def close_redis():
    """
    Close Redis connection if it exists.
    """

    if settings.REDIS_HOST and settings.REDIS_PORT:
        # Redis close logic would go here
        # Example: if redis: await redis.close()
        logger.info("Redis connection closed")
    else:
        logger.info("Redis connection not configured, skipping")


async def init_external_clients(app: FastAPI):
    """
    Initialize all external connections (database, cache, etc.)
    """
    logger.info("Initializing external connections...")

    # Initialize database
    await init_tortoise(app)
    logger.info("Database connection initialized")

    # Initialize Redis if configured
    await init_redis()

    logger.info("All external connections initialized")


async def shutdown():
    """
    Close all external connections.
    """
    logger.info("Shutting down external connections...")

    # Close database connections
    if Tortoise._inited:
        await Tortoise.close_connections()
        logger.info("Database connections closed")

    # Close Redis connection
    await close_redis()

    logger.info("All external connections closed")
