from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Annotated
import models
from models import User, Todo
from sqlalchemy.orm import Session
from database import SessionLocal, engine



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
    user_id: str

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

@app.get("/")
async def root():
    return {"message": "My Todo App"}


@app.post("/user/signup")
async def sign_up(user: UserBase, db: db_dependency):
    try:
        user.password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        user = User(**user.model_dump())
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"message":"user registered successfully!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    
@app.get("/user/login")
async def login(user: UserBase, db: db_dependency):
    try:
        user_data: User or None = db.query(User).filter(User.email == user.email).first()
        if user_data:
            isCorrectPassword:bool = bcrypt.checkpw(user.password, user_data.password)
        else:
            return {"message":"Invalid password"}
    except Exception as e:
        return

@app.post("/todo/create")
async def create_todo(todo: TodoBase, db: db_dependency):
    try:
        todo = Todo(**todo.model_dump())
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return {"message":"todo created successfully!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

@app.get("/todo/{user_id}")
async def get_todos(user_id: str, db: db_dependency):
    try:
        todos = db.query(Todo).filter(Todo.user_id == user_id).first()
        return {"todos":todos}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

@app.patch("/todo/update/{todo_id}")
async def update_todo(todo_id: str, todo: TodoBase, db: db_dependency):
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
async def delete_todo(todo_id: str, db: db_dependency):
    try:
        db.query(Todo).filter(Todo.id == todo_id).delete()
        db.commit()
        return {"message":"Todo deleted successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    
