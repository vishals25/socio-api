from fastapi import Body, FastAPI,Response,status,HTTPException,Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,schemas,utils
from .database import engine,get_db
from typing import List

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

@app.get("/")
def root():
    return "Hello World"

@app.get("/posts",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):

    posts=db.query(models.Post).all()
    return posts


@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db)):

    new_post=models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) 

    return new_post

@app.get("/posts/{id}",response_model=schemas.Post)
def get_posts(id:int,db: Session = Depends(get_db)):

    post=db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found")
    return post


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db)):

    post=db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id {id} not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


    
@app.put("/posts/{id}",response_model=schemas.Post)

def update_posts(id:int,updated_post:schemas.PostCreate,db: Session = Depends(get_db)):

    post_query=db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id {id} not found")
    
    post_query.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()
    
    return post_query.first()

@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)

def create_user(user : schemas.UserCreate,db: Session = Depends(get_db)):

    #hash the password

    hashed_password=utils.hash(user.password)
    user.password=hashed_password

    new_user=models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 

    return new_user

@app.get("/users/{id}",response_model=schemas.UserOut)

def get_user(id:int,db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with id : {id} not found !")
    return user