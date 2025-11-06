from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from app.database import Base
from datetime import datetime

class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)  
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)  
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  

    user_id = Column(Integer, ForeignKey('users.id'))  

    user = relationship("User", back_populates="todos")