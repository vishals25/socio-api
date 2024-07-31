from typing import Optional
from fastapi import Body, FastAPI,Response,status,HTTPException
from pydantic import BaseModel
from random import randrange

app=FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating:Optional[int]=None

# Path Operation 

my_posts = [{
    "title": "Post 1",
    "content": "This is post 1",
    "id": 1
},{
    "title": "Post 2",
    "content": "This is post 2",
    "id": 2
}]


def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p

def remove_post(id):
    for p in my_posts:
        if p['id']==id:
            my_posts.remove(p)
            return True

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i

@app.get("/")
def root():
    return "Hello World"


@app.get("/posts")
def get_posts():
    return my_posts


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):

    post_dict=post.model_dump()
    post_dict['id']=randrange(0,100000000)
    my_posts.append(post_dict)
    return {"post":my_posts}

@app.get("/posts/{id}")
def get_posts(id:int,response=Response):
    post=find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    return post


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # To remove the particular Post
    #index=find)index_post(id)
    if not remove_post(id):
    # if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id {id} not found")
    # my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.put("/posts/{id}")

def update_posts(id:int,post:Post):
    # To update the particular Post
    index=find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id {id} not found")
    post_dict=post.model_dump()
    post_dict['id']=id
    my_posts[index]=post_dict
    return {"post_details":post_dict}
    