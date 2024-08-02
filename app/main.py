from typing import Optional
from fastapi import Body, FastAPI,Response,status,HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app=FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# Path Operation 

while True:
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='vishal',cursor_factory=RealDictCursor,)

        # Open a cursor to perform database operations
        cur = conn.cursor()
        print("Database Connection Successfull!")

        break

    except Exception as e:
        print("Database Connection Failed!")
        print("Error :",e)
        time.sleep(3)
        

@app.get("/")
def root():
    return "Hello World"


@app.get("/posts")
def get_posts():
    cur.execute("""SELECT * FROM posts""")
    records = cur.fetchall()
    return records


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    
    cur.execute("""insert into posts (title,content,published) values (%s,%s,%s) returning * """,(post.title,post.content,post.published))
    new_post=cur.fetchone()
    conn.commit()
    return {"post Created ":new_post}

@app.get("/posts/{id}")
def get_posts(id:int):
    cur.execute("""SELECT * FROM posts where id = %s """,(str(id),))
    post = cur.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found")
    return post


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cur.execute("""delete from posts where id = %s returning * """,(str(id),))
    deleted_post=cur.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.put("/posts/{id}")

def update_posts(id:int,post:Post):

    cur.execute("""update posts set title= %s,content= %s,published=%s where id = %s returning *""",(post.title,post.content,post.published,str(id)))
    updated_post=cur.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id {id} not found")
    
    return {"post_details":updated_post}