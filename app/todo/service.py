from sqlalchemy.orm import Session
from app.todo.models import Todo
from app.models import User
from app.todo.schemas import TodoCreate, TodoUpdate
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException


def create_todo(db: Session, todo: TodoCreate, user_email: str):
    db_user = db.query(User).filter(User.email == user_email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        user_id=db_user.id  
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todos(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(Todo).filter(Todo.user_id == user_id).offset(skip).limit(limit).all()

def get_todo_by_id(db: Session, todo_id: int, user_id: int):
    return db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()

def update_todo(db: Session, todo_id: int, todo_update: TodoUpdate, user_id: int):
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()
    if db_todo:
        db_todo.title = todo_update.title
        db_todo.description = todo_update.description
        db_todo.completed = todo_update.completed
        db.commit()
        db.refresh(db_todo)
        return db_todo
    return None

def delete_todo(db: Session, todo_id: int, user_id: int):
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
        return db_todo
    return None