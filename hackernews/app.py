from contextlib import asynccontextmanager

from fastapi import FastAPI

from hackernews.models.db import create_db_and_tables
from hackernews.routes.auth import auth_router
from hackernews.routes.posts import posts_router
from hackernews.routes.users import users_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown


app = FastAPI(lifespan=lifespan)


@app.get("/ping")
async def pong():
    return {"ping": "pong"}


app.include_router(posts_router)
app.include_router(users_router)
app.include_router(auth_router)
