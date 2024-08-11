from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime

class UserLogin(BaseModel):
    email:EmailStr
    password:str
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

# class Owner(BaseModel):
#     email:EmailStr
class Post(PostBase):
    id:int
    owner_id:int
    created_at: datetime
    owner:UserOut

class Token(BaseModel):
    access_token: str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]=None

class Vote(BaseModel):
    post_id:int
    dir: conint(ge=0, le=1) # type: ignore
    
class PostOut(BaseModel):
    Post:Post
    votes:int