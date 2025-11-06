from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models import Base, User as UserModel
from app.auth.schemas import UserCreate, UserLogin
from app.auth.auth import hash_password, verify_password
from app.auth.jwt import create_access_token, verify_token
from app.todo.router import router as todo_router

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=UserCreate)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(UserModel).filter(UserModel.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(user.password)
    db_user = UserModel(first_name=user.first_name, last_name=user.last_name,
                        email=user.email, password=hashed)
    db.add(db_user); db.commit(); db.refresh(db_user)
    return user  


@app.post("/token")
def login_for_access_token(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = verify_token(token)
    return {"email": user.email}

@app.get("/secure-data")
async def get_secure_data(token: str = Depends(oauth2_scheme)):
    return {"message": "This is secured data", "token": token}
app.include_router(todo_router)