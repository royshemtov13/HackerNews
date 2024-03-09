from sqlmodel import Field, SQLModel


class Posts(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    content: str
    upvotes: int = Field(default=0)
