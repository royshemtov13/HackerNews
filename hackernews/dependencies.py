from sqlmodel import Session

from hackernews.models.db import engine


def get_session() -> Session:
    return Session(engine)
