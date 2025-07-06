from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email : EmailStr
    password: str = Field(min_length=8, max_length=64)
    first_name: str
    last_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    custom_token: str