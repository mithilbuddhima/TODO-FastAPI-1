from sqlalchemy.orm import Session
from app.models import User
import bcrypt  


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_person(db: Session, user_data: dict):
    hashed_password = hash_password(user_data['password']) 
    
    user = User(
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
        email=user_data['email'],
        password=hashed_password  
    )
    
    db.add(user)
    db.commit()
    db.refresh(user) 
    
    return user