from pydantic import BaseModel


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

    class Config:
        orm_mode = True  

class UserLogin(BaseModel):
    email: str
    password: str