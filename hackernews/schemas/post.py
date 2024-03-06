from pydantic import BaseModel


class PostCreate(BaseModel):
    content: str


class PostResponse(BaseModel):
    id: int
    content: str
    upvotes: int = 0
