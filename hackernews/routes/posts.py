from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from hackernews.dependencies import get_session
from hackernews.models.post import Post
from hackernews.schemas.post import PostResponse

posts_router = APIRouter(prefix="/posts")


@posts_router.get("/")
def get_posts(session: Session = Depends(get_session)) -> list[PostResponse]:
    with session as db:
        statement = select(Post)
        posts = db.exec(statement).all()
        return [
            PostResponse(id=post.id, content=post.content, upvotes=post.upvotes)
            for post in posts
        ]
