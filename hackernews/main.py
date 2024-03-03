from fastapi import FastAPI, HTTPException

from hackernews import database, models

app = FastAPI()

database.init()


@app.get("/posts", response_model=list[models.Post])
async def read_posts():
    posts = await database.get_posts()
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found")
    return posts
