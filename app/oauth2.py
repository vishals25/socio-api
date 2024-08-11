from datetime import timedelta,datetime,timezone
from fastapi import Depends,status,HTTPException
from jose import JWTError, jwt
from . import schemas,database,models
from sqlalchemy.orm import Session
from .config import settings

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY
#Algorithms
#Expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
access_token_expire_minutes = settings.access_token_expire_minutes

def create_access_data(data:dict):

    to_encode=data.copy()

    expire=datetime.now(timezone.utc) + timedelta(minutes=access_token_expire_minutes)
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