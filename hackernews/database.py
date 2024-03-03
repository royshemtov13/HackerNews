import databases
import sqlalchemy
from sqlalchemy import select

DATABASE_URL = "postgresql://username:password@localhost/hackersnews"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

posts = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("content", sqlalchemy.string),
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)


async def init():
    await database.connect()


async def get_posts():
    query = select([posts])
    return await database.fetch_all(query)
