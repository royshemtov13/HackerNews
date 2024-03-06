from functools import cache

import sqlalchemy
from sqlmodel import SQLModel, create_engine

from hackernews.models.post import Post  # noqa
from hackernews.settings import settings


def get_connection_string(
    username: str,
    password: str,
    host: str,
    port: int,
    db_name: str,
):
    return f"postgresql://{username}:{password}@{host}:{port}/{db_name}"


@cache
def get_engine(connection_string: str) -> sqlalchemy.Engine:
    return create_engine(connection_string)


engine = get_engine(
    connection_string=get_connection_string(
        settings.db_user,
        settings.db_password,
        settings.db_host,
        settings.db_port,
        settings.db_name,
    )
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine, checkfirst=True)
