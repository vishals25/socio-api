from datetime import timedelta,datetime,timezone
from fastapi import Depends,status,HTTPException
from jose import JWTError, jwt
from . import schemas,database,models
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY
#Algorithms
#Expiration time

SECRET_KEY = "vcgaAaBgbpIj29uzPATrEusWn2GueJR7xoejUyNdUlBFTv+NPz6C85fQ9o/avW5mjTeCx01iN7LjCkGDpL/TNTfLyH7pLir3"

ALGORITHM = "HS256"
EXPIRATION_DELTA = 60

def create_access_data(data:dict):

    to_encode=data.copy()

    expire=datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_DELTA)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token:str,credentials_exception):

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        id:str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=str(id))
    
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token : str =Depends(oauth2_scheme),db :Session=Depends(database.get_db)):
    cretendials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail="Could not validate credentials",
                                        headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token,cretendials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user