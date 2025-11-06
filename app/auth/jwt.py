from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Union
from app.models import User as UserModel
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def verify_token(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise JWTError("Could not validate credentials")
        
        user = db.query(UserModel).filter(UserModel.email == email).first()
        
        if user is None:
            raise JWTError("User not found")
        
        return user  
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token")