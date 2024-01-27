from fastapi import FastAPI, Depends, HTTPException, status, Response, Cookie, Request
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Annotated
import models
from models import User, Todo
from sqlalchemy.orm import Session
import ast
import json
from database import SessionLocal, engine
from auth import get_password_hash, verify_password, create_access_token, TokenData, verify_access_token, oauth2_scheme, Token

app: FastAPI = FastAPI()
models.Base.metadata.create_all(bind=engine)


def validate_password_length(value):
    if len(value) < 8:
        raise ValueError("Password must be at least 8 characters")
    return value
    
class TodoBase(BaseModel):
    title: str
    description: str
    isDone: bool = Field(default=False)
    # user_id: str

class UserBase(BaseModel):
    email: EmailStr
    password: str

    _validate_password_length = validator("password", pre=True, always=True)(validate_password_length)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# @app.get("/get-cookie")
def get_cookie(request: Request, session: str = Cookie(None)) -> str:
    auth = request.headers.get("authorization", "")
    if session is None and auth == '':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if session is not None:
        _session = json.loads(session.replace("'", "\""))
        return _session.get("access_token", "")
    else:
        __session = ast.literal_eval(auth.replace('Bearer ', ''))
        return __session.get("access_token", "")

# def get_current_user(token: str = Depends(oauth2_scheme), db = db_dependency) -> User:
def get_current_user(db: db_dependency, access_token = Depends(get_cookie)) -> User:
    credentials_exception: HTTPException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                         detail="Could not validate credentials",
                                                         headers = {
                                                             "WWW-Authenticate": "Bearer",
                                                             }
                                                             )
    token:TokenData = verify_access_token(access_token, credentials_exception)
    user: User = db.query(User).filter(User.id == token.id).first()
    return user

@app.get("/")
async def root():
    return {"message": "My Todo App"}


@app.post("/user/signup")
async def sign_up(user: UserBase, db: db_dependency):
    try:
        userExist = db.query(User).filter(User.email == user.email).first()
        if userExist is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User with this email already exists")
        user.password = get_password_hash(user.password)
        user = User(**user.model_dump())
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"message":"User registered successfully!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    
@app.post("/user/login")
async def login(user: UserBase, db: db_dependency, response: Response):
    try:
        user_data: User or None = db.query(User).filter(User.email == user.email).first()
        if user_data:
            if verify_password(user.password, user_data.password):
                session: Token = create_access_token({"id":user_data.id})
                response.set_cookie(key='session', value=session, httponly=True, samesite="none", secure=True)
                return {"message":"User logged in successfully!", "session":session}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password.")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid email or password.")
    except Exception as e:
        return {"message":str(e)}

@app.post("/todo/create")
async def create_todo(todo: TodoBase, db: db_dependency, user: User = Depends(get_current_user)):
    try:
        todo_data = todo.model_dump()
        todo_data["user_id"] = user.id
        todo = Todo(**todo_data)
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return {"message":"todo created successfully!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


# Returns the todos of the user
@app.get("/todos/get")
async def get_todos(db: db_dependency, user: User = Depends(get_current_user)):
    try:
        todos:list[Todo] = db.query(Todo).filter(Todo.user_id == user.id).all()
        if todos:
            return {"todos": [todo for todo in todos]}
        else:
            return {"message":"No todos found"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

@app.patch("/todo/update/{todo_id}")
async def update_todo(todo_id: str, todo: TodoBase, db: db_dependency, user: User = Depends(get_current_user)):
    try:
        old_todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if old_todo:
            old_todo.title = todo.title
            old_todo.description = todo.description
            old_todo.isDone = todo.isDone
            db.commit()
            return {"message":"Todo updated successfully."}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

@app.delete("/todo/delete/{todo_id}")
async def delete_todo(todo_id: str, db: db_dependency, user: User = Depends(get_current_user)):
    try:
        db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user.id).delete()
        db.commit()
        return {"message":"Todo deleted successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    
