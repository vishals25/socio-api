from datetime import timedelta,datetime
from jose import JWTError, jwt
from . import schemas

#SECRET_KEY
#Algorithms
#Expiration time

SECRET_KEY = "vcgaAaBgbpIj29uzPATrEusWn2GueJR7xoejUyNdUlBFTv+NPz6C85fQ9o/avW5mjTeCx01iN7LjCkGDpL/TNTfLyH7pLir3"

ALGORITHM = "HS256"
EXPIRATION_DELTA = 30

def create_access_data(data:dict):

    to_encode=data.copy()

    expire=datetime.now() + timedelta(minutes=EXPIRATION_DELTA)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token:str,credentials_exception):

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithm=ALGORITHM)

        id:str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)
    
    except JWTError:
        raise credentials_exception

def get_current_user():
    pass