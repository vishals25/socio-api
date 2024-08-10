from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas,models,utils,oauth2

router=APIRouter(
    tags=['Authenticate']
)

@router.post("/login")
def login(user_credentials:OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    

    # create a token
    access_token=oauth2.create_access_data(data={"user_id":user.id})
    # return token
    return{"access_token":access_token,
           "token_type":"bearer"
           }