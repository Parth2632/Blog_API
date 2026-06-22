from jose import jwt, JWTError
from datetime import datetime,timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("secretkey")
algorithm = os.getenv("algorithm")
access_token_expire_minutes = int(os.getenv("accesstokentime"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = access_token_expire_minutes)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=algorithm)
    return encoded_jwt    

def verify_token(token:str=Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=algorithm)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401,detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid token")
    