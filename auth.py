from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status

load_dotenv()

#  User Auth JWT

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_content:CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CustomOAuthPasswordForm (OAuth2PasswordRequestForm):
    email: str

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/user/login")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_content.verify(plain_password, hashed_password)

def get_password_hash(password) -> str:
    return pwd_content.hash(password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire:datetime = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) 
    to_encode.update({"exp": expire})
    encoded_jwt:str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token":encoded_jwt, "token_type":"bearer"}


def verify_access_token(token: str, credentials_exception: HTTPException) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY=SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("id")
        if id is None:
            raise credentials_exception
        token_data:TokenData = TokenData(id=id)
    except JWTError as e:
        print(e)
        raise credentials_exception
    return token_data
