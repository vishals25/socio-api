from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app=FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating:Optional[int]=None

# Path Operation 

@app.get("/")
def root():
    return "Hello World"


@app.get("/posts")
def get_posts():
    return [{"title": "Post 1", "content": "Content of post 1"},
            {"title": "Post 2", "content": "Content of post 2"}]


@app.post("/createposts")
def create_posts(post:Post):

    # title -> str,# content -> str
    print(post.model_dump())
    return {"post": f"{post}"}