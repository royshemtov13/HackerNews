from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from hackernews.dependencies import get_session
from hackernews.models.user import Users
from hackernews.schemas.user import UserCreate, UserResponse
from hackernews.utils import hash_password

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    session: Session = Depends(get_session),
) -> UserResponse:

    user.password = hash_password(user.password)

    u = Users(email=user.email, password=user.password)
    with session as db:
        db.add(u)
        db.commit()
        db.refresh(u)
    return UserResponse(id=u.id, email=u.email)


@users_router.get("/{user_id}")
def get_user(user_id: int, session: Session = Depends(get_session)) -> UserResponse:
    with session as db:
        statement = select(Users).where(Users.id == user_id)
        user = db.exec(statement).one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(id=user.id, email=user.email)
