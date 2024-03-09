from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session, asc, desc, select, update

from hackernews.dependencies import get_session
from hackernews.models.post import Posts
from hackernews.schemas.post import PostCreate, PostResponse

posts_router = APIRouter(prefix="/posts", tags=["posts"])


@posts_router.get("/")
def get_posts(
    session: Session = Depends(get_session),
    limit: int = 10,
    skip: int = 0,
    descending: bool = True,
) -> list[PostResponse]:
    with session as db:
        order = desc(Posts.upvotes) if descending else asc(Posts.upvotes)
        statement = select(Posts).order_by(order).limit(limit=limit).offset(skip)
        posts = db.exec(statement).all()
        return [
            PostResponse(id=post.id, content=post.content, upvotes=post.upvotes)
            for post in posts
        ]


@posts_router.get("/{post_id}")
def get_post(post_id: int, session: Session = Depends(get_session)) -> PostResponse:
    with session as db:
        statement = select(Posts).where(Posts.id == post_id)
        post = db.exec(statement).one_or_none()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return PostResponse(
            id=post.id,
            content=post.content,
            upvotes=post.upvotes,
        )


@posts_router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate, session: Session = Depends(get_session)
) -> PostResponse:
    p = Posts(content=post.content)
    with session as db:
        db.add(p)
        db.commit()
        db.refresh(p)
    return PostResponse(id=p.id, content=p.content, upvotes=p.upvotes)


@posts_router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, session: Session = Depends(get_session)) -> Response:
    with session as db:
        statement = select(Posts).where(Posts.id == post_id)
        p = db.exec(statement).one_or_none()
        if not p:
            raise HTTPException(status_code=404, detail="Post not found")
        db.delete(p)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@posts_router.put("/upvotes/{post_id}", status_code=status.HTTP_201_CREATED)
def upvote_post(post_id: int, session: Session = Depends(get_session)) -> PostResponse:
    with session as db:
        statement = (
            update(Posts).where(Posts.id == post_id).values(upvotes=Posts.upvotes + 1)
        )
        result = db.exec(statement)

        if not result.rowcount:
            raise HTTPException(status_code=404, detail="Post not found")

        post = select(Posts).where(Posts.id == post_id)
        post = db.exec(post).first()
        db.commit()
        db.refresh(post)

        return PostResponse(
            id=post.id,
            content=post.content,
            upvotes=post.upvotes,
        )
