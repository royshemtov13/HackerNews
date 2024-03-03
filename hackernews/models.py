from pydantic import BaseModel


class Post(BaseModel):
    id: int
    content: str

    class Config:
        orm_mode = True
