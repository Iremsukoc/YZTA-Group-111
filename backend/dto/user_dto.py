from pydantic import BaseModel, EmailStr, Field

class CreateUserDTO(BaseModel):
    email : EmailStr
    password: str = Field(min_length=8, max_length=64)
    first_name: str
    last_name: str
