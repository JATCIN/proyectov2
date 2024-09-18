from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    full_name: str
    password: str

class UserResponse(BaseModel):
    email: str
    full_name: str

    class Config:
        orm_mode = True