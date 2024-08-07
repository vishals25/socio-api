from fastapi import Body, FastAPI,Response,status,HTTPException,Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,schemas 
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine)


app=FastAPI()



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
def get_posts(db: Session = Depends(get_db)):
    # cur.execute("""SELECT * FROM posts""")
    # records = cur.fetchall()
    posts=db.query(models.Post).all()
    return {"data":posts}


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db)):
    
    # cur.execute("""insert into posts (title,content,published) values (%s,%s,%s) returning * """,(post.title,post.content,post.published))
    # new_post=cur.fetchone()
    # conn.commit()

    new_post=models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) 

    return {"post Created ":new_post}

@app.get("/posts/{id}")
def get_posts(id:int,db: Session = Depends(get_db)):
    # cur.execute("""SELECT * FROM posts where id = %s """,(str(id),))
    # post = cur.fetchone()
    post=db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found")
    return post


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db)):

    # cur.execute("""delete from posts where id = %s returning * """,(str(id),))
    # deleted_post=cur.fetchone()
    # conn.commit()

    post=db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id {id} not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


    
@app.put("/posts/{id}")

def update_posts(id:int,updated_post:schemas.PostCreate,db: Session = Depends(get_db)):

    # cur.execute("""update posts set title= %s,content= %s,published=%s where id = %s returning *""",(post.title,post.content,post.published,str(id)))
    # updated_post=cur.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id {id} not found")
    
    post_query.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()
    
    return {"post_details":post_query.first()}