from contextlib import asynccontextmanager

from fastapi import FastAPI

from hackernews.models.db import create_db_and_tables
from hackernews.routes.posts import posts_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown


app = FastAPI(lifespan=lifespan)


app.include_router(posts_router)
