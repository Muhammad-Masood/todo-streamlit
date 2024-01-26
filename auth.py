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
    exp: datetime

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_content.verify(plain_password, hashed_password)

def get_password_hash(password) -> str:
    return pwd_content.hash(password)

def create_access_token(data: dict) -> Token:
    to_encode = data.copy()
    expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) 
    to_encode.update({"exp": expire})
    encoded_jwt:str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token":encoded_jwt, "token_type":"bearer"}


def verify_access_token(token: str, credentials_exception: HTTPException) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data: TokenData = TokenData(**payload)
        if token_data.id is None:
            raise credentials_exception
        # Ensure datetime.utcnow() is aware of the UTC timezone
        current_time = datetime.utcnow().replace(tzinfo=timezone.utc)

        if token_data.exp is not None and current_time > token_data.exp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError as e:
        print(e)
        raise credentials_exception
    return token_data
