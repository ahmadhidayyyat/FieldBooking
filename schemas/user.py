from pydantic import BaseModel, Field
from typing import List, Optional
from .booking import BookingResponse

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r"^\S+@\S+\.\S+$")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserResponse(UserBase):
    id: int
    bookings: List[BookingResponse] = []

    class Config:
        from_attributes = True
