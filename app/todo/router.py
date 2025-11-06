from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.todo import service
from app.todo.schemas import TodoCreate, TodoUpdate, Todo
from app.auth.jwt import verify_token  
from app.models import User
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = verify_token(token, db)  
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user


@router.post("/todos/", response_model=Todo)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return service.create_todo(db=db, todo=todo, user_email=current_user.email)


@router.get("/todos/", response_model=list[Todo])
def get_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return service.get_todos(db=db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/todos/{todo_id}", response_model=Todo)
def get_todo_by_id(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo = service.get_todo_by_id(db=db, todo_id=todo_id, user_id=current_user.id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo = service.update_todo(db=db, todo_id=todo_id, todo_update=todo_update, user_id=current_user.id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@router.delete("/todos/{todo_id}", response_model=Todo)
def delete_todo(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo = service.delete_todo(db=db, todo_id=todo_id, user_id=current_user.id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo