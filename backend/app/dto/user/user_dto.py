from pydantic import BaseModel, Field
from typing import Optional

class UpdateUserProfileDTO(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1)
    last_name: Optional[str] = Field(None, min_length=1)
    phone_number: Optional[str] = Field(None, description="User's phone number")
    dob: Optional[str] = Field(None, description="Date of birth in YYYY-MM-DD format")
    gender: Optional[str] = Field(None, description="User's gender")

class ChangePasswordDTO(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)